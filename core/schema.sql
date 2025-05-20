DROP TABLE IF EXISTS user_term_progress;
DROP TABLE IF EXISTS user_sets;
DROP TABLE IF EXISTS terms;
DROP TABLE IF EXISTS sets;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE sets (
    set_id SERIAL PRIMARY KEY,
    creator_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    parent_set_id INTEGER REFERENCES sets(set_id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
);

CREATE TABLE terms (
    term_id SERIAL PRIMARY KEY,
    set_id INTEGER NOT NULL REFERENCES sets(set_id) ON DELETE CASCADE,
    word TEXT NOT NULL,
    definition TEXT NOT NULL,
    order_in_set INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_sets (
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    set_id INTEGER NOT NULL REFERENCES sets(set_id) ON DELETE CASCADE,
    last_accessed_at TIMESTAMP,
    added_at TIMESTAMP DEFAULT NOW(),
    starred BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (user_id, set_id)
);

CREATE TABLE user_term_progress (
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    term_id INTEGER NOT NULL REFERENCES terms(term_id) ON DELETE CASCADE,
    repetitions INTEGER DEFAULT 0,
    starred BOOLEAN DEFAULT FALSE,
    difficulty FLOAT CHECK (difficulty BETWEEN 0 AND 5),
    last_practiced_at TIMESTAMP,
    PRIMARY KEY (user_id, term_id)
);

CREATE TABLE set_ratings (
    set_id INTEGER REFERENCES sets(set_id),
    user_id INTEGER REFERENCES users(user_id),
    stars INTEGER CHECK (stars BETWEEN 1 AND 5),
    PRIMARY KEY (set_id, user_id)
);