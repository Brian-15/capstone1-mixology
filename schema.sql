DROP DATABASE IF EXISTS mixology;
CREATE DATABASE mixology;

\c mixology

CREATE TABLE languages
(
    id   SERIAL PRIMARY KEY,
    code TEXT UNIQUE
);

INSERT INTO languages(code) VALUES('EN'), ('DE'), ('ES'), ('FR'), ('IT');

CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT NOT NULL,
    language_pref INTEGER REFERENCES languages
);

CREATE TABLE categories
(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE glasses
(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE instructions
(
    drink_id INTEGER REFERENCES drinks,
    language_id INTEGER REFERENCES languages,
    instruction TEXT NOT NULL,
    PRIMARY KEY(drink_id, language_id)
);

CREATE TABLE ingredients
(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE drinks_ingredients
(
    drink_id INTEGER REFERENCES drinks,
    ingredient_id INTEGER REFERENCES ingredients,
    quantity TEXT NOT NULL,
    PRIMARY KEY(drink_id, ingredient_id)
);

CREATE TABLE drinks
(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    image_url TEXT UNIQUE,
    image_attribution TEXT,
    video_url TEXT UNIQUE,
    alcoholic BOOLEAN NOT NULL,
    category_id INTEGER REFERENCES categories,
    glass_type_id INTEGER REFERENCES glasses
);

CREATE TABLE bookmarks
(
    user_id INTEGER REFERENCES users,
    drink_id INTEGER REFERENCES drinks,
    PRIMARY KEY(user_id, drink_id)
);