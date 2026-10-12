import pytest
from psycopg2 import errors


def test_database_version(db_cursor):
    db_cursor.execute("""
    SELECT version();
    """)
    row = db_cursor.fetchone()

    assert row is not None
    assert "PostgreSQL" in row[0]


def test_active_movies_count(db_cursor):
    db_cursor.execute("""
    SELECT COUNT(*) FROM movies
    WHERE is_available = TRUE
    """)
    row = db_cursor.fetchone()

    assert row[0] == 5


def test_movie_genres_relation_many_to_many(db_cursor):
    db_cursor.execute("""
    SELECT movies.title, genres.name FROM movies
    JOIN movie_genres ON movies.id = movie_genres.movie_id
    JOIN genres ON movie_genres.genre_id = genres.id
    WHERE movies.title = 'Aliens';
    """)
    rows = db_cursor.fetchall()

    assert len(rows) == 2
    genre_names = [row[1] for row in rows]
    assert "Sci-Fi" in genre_names
    assert "Horror" in genre_names


def test_insert_movie_transaction_isolation(db_cursor):
    insert_movie = ("Blade Runner", 1982, 7.7, True)
    query = """
    INSERT INTO movies (title, release_year, rating, is_available)
    VALUES(%s, %s, %s, %s);
    """
    db_cursor.execute(query, insert_movie)
    db_cursor.execute("""
    SELECT title, release_year, rating, is_available FROM movies
    WHERE title = 'Blade Runner';
    """)
    row = db_cursor.fetchone()

    assert row[0] == "Blade Runner"
    assert row[1] == 1982
    assert float(row[2]) == 7.7
    assert row[3] is True


def test_insert_invalid_genre_id_fails(db_cursor):
    with pytest.raises(errors.ForeignKeyViolation):
        db_cursor.execute("""
        INSERT INTO movie_genres (movie_id, genre_id)
        VALUES (1, 666);
        """)

def test_genres_movie_count_aggregation(db_cursor):
    db_cursor.execute("""
    SELECT g.name, COUNT(mg.movie_id) AS total_movies
    FROM genres g
    JOIN movie_genres mg ON g.id = mg.genre_id
    GROUP BY g.name
    ORDER BY total_movies DESC;
    """)
    rows = db_cursor.fetchall()
    
    genre_names = [row[0] for row in rows]
    counts = [row[1] for row in rows]
    assert genre_names[0] == "Sci-Fi"
    assert counts[0] == 6
    assert all(c >= 2 for c in counts)


def test_update_movie_rating_lifecycle(db_cursor):
    query = """
    UPDATE movies
    SET rating = %s
    WHERE title = %s
    """
    db_cursor.execute(query, (8.8, 'Interstellar'))
    assert db_cursor.rowcount == 1
    
    db_cursor.execute("""
    SELECT rating FROM movies
    WHERE title = 'Interstellar';
    """)
    row = db_cursor.fetchone()

    assert row[0] is not None
    assert float(row[0]) == 8.8


def test_duplicate_movie_title_fails(db_cursor):
    with pytest.raises(errors.UniqueViolation):
        shining = ("The Shining", 1980, 7.8)
        query = """
        INSERT INTO movies (title, release_year, rating)
        VALUES (%s, %s, %s);
        """
        db_cursor.execute(query, shining)