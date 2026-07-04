from app.database.connection import get_connection

SCHEMA= """
CREATE TABLE IF NOT EXISTS comments (
    id BIGSERIAL PRIMARY KEY,
    video_id TEXT,
    text TEXT,
    text_processed TEXT,
    label INT
);
"""

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(SCHEMA)

    conn.commit()
    cursor.close()
    conn.close()

    print("Database initialized ✅")


if __name__ == "__main__":
    init_db()