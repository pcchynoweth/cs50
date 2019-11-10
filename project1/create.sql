DROP TABLE authors IF EXISTS;

CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    author VARCHAR NOT NULL
);

DROP TABLE books IF EXISTS;

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author_id INTEGER REFERENCES authors,
    year INTEGER 
);

