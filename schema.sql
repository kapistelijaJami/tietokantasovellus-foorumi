CREATE TABLE area (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    created_at TIMESTAMP
);

CREATE TABLE thread (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    created_at TIMESTAMP,
	area_id INTEGER REFERENCES area
);

CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    msg TEXT,
    sent_at TIMESTAMP,
	thread_id INTEGER REFERENCES thread
);

INSERT INTO area (topic, created_at) VALUES ('Ensimmäinen alue', NOW());
INSERT INTO area (topic, created_at) VALUES ('Toinen alue', NOW());