CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    UNIQUE(login)
);

CREATE INDEX users_login_idx ON users(login);

CREATE TABLE reviews (
    user_id INTEGER REFERENCES users(id),
    book_id TEXT NOT NULL,

    rating INTEGER NOT NULL CHECK(rating between 1 and 10),
    commentary TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    edited_at TIMESTAMP,

    UNIQUE(user_id, book_id)
);
