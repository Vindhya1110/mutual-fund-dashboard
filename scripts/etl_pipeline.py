from pathlib import Path
import pandas as pd
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def ingest_raw(raw_dir: Path):
    files = list(raw_dir.glob("*.csv"))
    if not files:
        logging.error("No CSV files found in %s", raw_dir)
        return {}

    tables = {}
    for f in files:
        try:
            df = pd.read_csv(f)
            # Normalise column names
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
            tables[f.stem] = df
            logging.info("Loaded %s (%s rows)", f.name, len(df))
        except Exception as e:
            logging.exception("Failed to read %s: %s", f, e)

    return tables


def basic_clean(tables: dict, processed_dir: Path):
    processed_dir.mkdir(parents=True, exist_ok=True)
    for name, df in tables.items():
        # Trim string columns (explicitly include pandas string dtype to
        # avoid Pandas4Warning when using newer pandas versions)
        str_cols = df.select_dtypes(include=["object", "string"]).columns
        for c in str_cols:
            df[c] = df[c].astype(str).str.strip()

        # Drop fully empty columns
        df = df.dropna(axis=1, how="all")

        out_path = processed_dir / f"{name}_clean.csv"
        df.to_csv(out_path, index=False)
        logging.info("Wrote processed: %s", out_path)


def load_sqlite(processed_dir: Path, db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        for csv in processed_dir.glob("*_clean.csv"):
            table_name = csv.stem.replace("_clean", "")
            df = pd.read_csv(csv)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            logging.info("Loaded table %s into %s", table_name, db_path.name)
    finally:
        conn.close()


def main():
    repo_root = Path.cwd()
    if repo_root.name == "notebooks":
        repo_root = repo_root.parent

    raw_dir = repo_root / "data" / "raw"
    processed_dir = repo_root / "data" / "processed"
    db_path = repo_root / "data" / "db" / "bluestock_mf.db"

    logging.info("Ingesting raw CSVs from %s", raw_dir)
    tables = ingest_raw(raw_dir)
    if not tables:
        logging.error("No tables ingested - aborting")
        return

    logging.info("Running basic cleaning and exporting processed CSVs")
    basic_clean(tables, processed_dir)

    logging.info("Loading processed CSVs into SQLite DB: %s", db_path)
    load_sqlite(processed_dir, db_path)


if __name__ == "__main__":
    main()
