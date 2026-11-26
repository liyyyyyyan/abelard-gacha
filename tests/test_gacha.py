import unittest
from unittest.mock import patch

from app import draw_rarity


class DrawRarityTests(unittest.TestCase):
    @patch("app.secrets.randbelow", side_effect=[1, 0])
    def test_base_roll_can_award_five_star(self, _randbelow):
        self.assertEqual(draw_rarity(0, 0), (5, 0, 0))

    @patch("app.secrets.randbelow", side_effect=[1, 1])
    def test_base_rate_is_one_in_one_thousand(self, _randbelow):
        self.assertEqual(draw_rarity(0, 0), (4, 0, 1))

    @patch("app.secrets.randbelow", side_effect=[1, 999])
    def test_hard_pity_awards_five_star_on_hundredth_pull(self, _randbelow):
        self.assertEqual(draw_rarity(3, 99), (5, 0, 0))

    @patch("app.secrets.randbelow", side_effect=[1, 999])
    def test_four_star_pity_does_not_award_five_star(self, _randbelow):
        self.assertEqual(draw_rarity(9, 50), (4, 0, 51))

    @patch("app.secrets.randbelow", return_value=0)
    def test_six_star_is_independent_and_preserves_five_star_pity(self, randbelow):
        self.assertEqual(draw_rarity(4, 20), (6, 0, 21))
        randbelow.assert_called_once_with(1_000)


if __name__ == "__main__":
    unittest.main()
