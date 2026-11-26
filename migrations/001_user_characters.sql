CREATE TABLE IF NOT EXISTS user_characters (
    user_id INT NOT NULL,
    character_id INT NOT NULL,
    copies INT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, character_id),
    CONSTRAINT fk_user_characters_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_characters_character
        FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
) ENGINE=InnoDB;
