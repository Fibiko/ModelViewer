"""create_db.py — создаёт SQLite БД ModelViewer по диаграмме (issue #11)."""
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(sys.argv[1] if len(sys.argv) > 1 else "modelviewer.db")

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Manufacturers (
    manufacturer_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_name  VARCHAR(100) NOT NULL,
    country_of_origin  VARCHAR(100),
    headquarters_city  VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Models (
    model_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name            VARCHAR(150) NOT NULL,
    screen_diagonal       DECIMAL(4,2),
    recommended_price     DECIMAL(10,2),
    benchmark_score       INTEGER,
    battery_capacity      INTEGER,
    manufacturer_id       INTEGER NOT NULL,
    release_year          SMALLINT,
    water_resistance      VARCHAR(20),
    matrix_type           VARCHAR(50),
    refresh_rate          INTEGER,
    pixel_density         INTEGER,
    brightness_nits       INTEGER,
    processor             VARCHAR(100),
    core_count            INTEGER,
    storage_capacity_gb   INTEGER,
    ram_capacity_gb       INTEGER,
    sim_slots_count       INTEGER,
    sd_slots_count        INTEGER,
    support_5g            BOOLEAN CHECK (support_5g IN (0, 1)),
    support_nfc           BOOLEAN CHECK (support_nfc IN (0, 1)),
    operating_system      VARCHAR(50),
    camera_resolution_mp  DECIMAL(6,2),
    FOREIGN KEY (manufacturer_id)
        REFERENCES Manufacturers (manufacturer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_models_manufacturer
    ON Models (manufacturer_id);
"""


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
    print(f"БД создана: {DB_PATH.resolve()}")
    print("Таблицы:", ", ".join(t[0] for t in tables))


if __name__ == "__main__":
    main()
