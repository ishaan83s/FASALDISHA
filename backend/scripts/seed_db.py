"""
CLI script to seed the database with initial catalog, prices, buyers, and demo weather scenarios.
Usage: python -m scripts.seed_db (from backend directory)
"""
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.seed.seed_data import seed_database

if __name__ == "__main__":
    print("Seeding FasalDisha database...")
    seed_database()
    print("Database seeding completed successfully.")
