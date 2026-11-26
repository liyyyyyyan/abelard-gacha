import unittest
from unittest.mock import patch

from app import app


class FakeCursor:
    def __init__(self):
        self.executed = []
        self.row = None
        self.rows = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def execute(self, query, params=None):
        self.executed.append((query, params))
        if "SELECT username FROM users" in query:
            self.row = {"username": "player"}
        elif "SELECT gems, pity4, pity5" in query:
            self.row = {"gems": 1000, "pity4": 0, "pity5": 0}
        elif "SELECT id, name, rarity, img FROM characters" in query:
            self.row = {
                "id": 12,
                "name": "Green",
                "rarity": 3,
                "img": "images/Green.png",
            }
        elif "FROM user_characters uc" in query:
            self.rows = [
                {
                    "name": "Green",
                    "rarity": 3,
                    "img": "images/Green.png",
                    "copies": 5,
                }
            ]

    def fetchone(self):
        return self.row

    def fetchall(self):
        return self.rows


class FakeConnection:
    def __init__(self):
        self.db_cursor = FakeCursor()
        self.committed = False

    def cursor(self):
        return self.db_cursor

    def commit(self):
        self.committed = True

    def rollback(self):
        pass

    def close(self):
        pass


class StoragePullTests(unittest.TestCase):
    def test_pull_records_character_and_returns_updated_storage(self):
        connection = FakeConnection()
        with patch("app.get_connection", return_value=connection), patch(
            "app.draw_rarity", return_value=(3, 0, 1)
        ):
            with app.test_client() as client:
                with client.session_transaction() as session:
                    session["id"] = 7

                response = client.post("/api/pull", data={"times": "1"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["storage"][0]["copies"], 5)
        self.assertTrue(connection.committed)
        self.assertTrue(
            any(
                "INSERT INTO user_characters" in query
                and "ON DUPLICATE KEY UPDATE copies = copies + 1" in query
                and params == (7, 12)
                for query, params in connection.db_cursor.executed
            )
        )
        self.assertTrue(
            any(
                "SELECT id, name, rarity, img FROM characters" in query
                and "name <> 'Beggar'" in query
                for query, _ in connection.db_cursor.executed
            )
        )

    def test_storage_has_its_own_authenticated_page(self):
        connection = FakeConnection()
        with patch("app.get_connection", return_value=connection):
            with app.test_client() as client:
                with client.session_transaction() as session:
                    session["id"] = 7

                response = client.get("/storage")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Character Storage", response.data)
        self.assertIn(b"Green", response.data)
        self.assertIn(b"5x", response.data)
        self.assertTrue(
            any(
                "FROM user_characters uc" in query
                and "c.name <> 'Beggar'" in query
                for query, _ in connection.db_cursor.executed
            )
        )


if __name__ == "__main__":
    unittest.main()
