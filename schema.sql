CREATE TABLE sections (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    access INTEGER DEFAULT 1
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    created_at TIMESTAMP,
    message TEXT,
    user_id INTEGER REFERENCES users,
    section_id INTEGER REFERENCES sections,
    visible INTEGER DEFAULT 1
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES threads,
    sent_at TIMESTAMP,
    answer TEXT,
    user_id INTEGER REFERENCES users,
    visible INTEGER DEFAULT 1
);

CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    answer_id INTEGER REFERENCES answers,
    user_id INTEGER REFERENCES users,
    vote INTEGER
);


INSERT INTO sections (name) VALUES ('Tietokoneet');
INSERT INTO sections (name, access) VALUES ('Häiriö käyttäjät', 2);