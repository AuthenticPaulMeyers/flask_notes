-- Create and save notes
-- Entities:
-- 1. users
-- 2. notes
-- 3. category

-- CREATE TABLE users(
--     id INTEGER,
--     username TEXT UNIQUE NOT NULL,
--     email TEXT UNIQUE NOT NULL,
--     password TEXT,
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
--     PRIMARY KEY(id)
--     );

-- CREATE TABLE notes(
--     id INTEGER,
--     user_id INTEGER,
--     title TEXT,
--     content TEXT,
--     category_id INTEGER,
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
--     PRIMARY KEY(id),
--     FOREIGN KEY(category_id) REFERENCES category(id),
--     FOREIGN KEY(user_id) REFERENCES users(id)
--     );

-- CREATE TABLE category(
--     id INTEGER,
--     name TEXT,
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
--     PRIMARY KEY(id)
--     );


-- INSERT INTO category(name) VALUES('Personal'), ('School'), ('Diary'), ('Church'), ('Other');

-- SELECT * FROM category;



-- INSERT INTO users(username, email, password) VALUES ('alice', 'alicy@example.com', 'licy');