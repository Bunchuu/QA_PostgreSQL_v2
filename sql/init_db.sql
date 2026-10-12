DROP TABLE IF EXISTS movie_genres;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS genres;

CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) UNIQUE NOT NULL,
    release_year INTEGER NOT NULL,
    rating NUMERIC(3, 1) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE movie_genres (
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);

INSERT INTO genres (name)
VALUES
    ('Sci-Fi'),
    ('Action'),
    ('Horror');

INSERT INTO movies (
    title, release_year, rating, is_available
) VALUES
    ('Escape from New York', 1981, 6.8, TRUE),
    ('Halloweeen', 1978, 6.8, FALSE),
    ('Commando', 1985, 6.7, TRUE),
    ('The Running Man', 1987, 6.6, FALSE),
    ('Total Recall', 1990, 7.2, FALSE),
    ('The Thing', 1982, 7.5, TRUE),
    ('Interstellar', 2014, 8.0, TRUE),
    ('Aliens', 1986, 7.6, FALSE),
    ('The Shining', 1980, 7.8, TRUE);

INSERT INTO movie_genres (
    movie_id, genre_id
    ) VALUES
    (1, 1), (1, 2),
    (2, 3),
    (3, 2),
    (4, 1), (4, 2),
    (5, 1), (5, 2),
    (6, 1), (6, 3),
    (7, 1),
    (8, 1), (8, 3),
    (9, 3);



