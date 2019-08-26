DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS frames;
DROP TABLE IF EXISTS players;

CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT DEFAULT "Game",
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE frames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    frame_number INTEGER NOT NULL,
    ball_one INTEGER NOT NULL DEFAULT 0,
    ball_two INTEGER NOT NULL DEFAULT 0,
    ball_three INTEGER NOT NULL DEFAULT 0,
    strike INTEGER NOT NULL DEFAULT 0,
    spare INTEGER NOT NULL DEFAULT 0,
    total_game_score INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (game_id) REFERENCES games (id),
    FOREIGN KEY (player_id) REFERENCES players (id)
);

CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (game_id) REFERENCES games (id)
);