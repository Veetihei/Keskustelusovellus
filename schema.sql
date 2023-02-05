CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    created_at TIMESTAMP,
    message TEXT
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES threads,
    sent_at TIMESTAMP,
    answer TEXT
);