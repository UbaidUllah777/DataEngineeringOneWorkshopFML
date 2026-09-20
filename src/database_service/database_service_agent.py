import os
import pandas as pd  # <-- Added missing pandas import
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import Json
import json

load_dotenv()


class DatabaseService:

	def __init__(self):
		self.database_url = os.getenv("DATABASE_URL")

		if not self.database_url:
			raise ValueError("DATABASE_URL was not found in .env")

	def create_table(self):
		connection = psycopg2.connect(self.database_url)

		try:
			cursor = connection.cursor()

			cursor.execute("""
				CREATE TABLE IF NOT EXISTS robot_data (
					record_id SERIAL PRIMARY KEY,
					record_data JSONB,
					inserted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
				)
			""")

			connection.commit()

		finally:
			cursor.close()
			connection.close()

	def insert_data(self, data_point):
		connection = psycopg2.connect(self.database_url)

		try:
			cursor = connection.cursor()

			record = data_point.to_dict(orient="records")[0]

			# Convert NaN values to None
			record = {
				key: None if pd.isna(value) else value
				for key, value in record.items()
			}

			cursor.execute(
				"""
				INSERT INTO robot_data (record_data)
				VALUES (%s)
				""",
				(Json(record),)
			)

			connection.commit()

		finally:
			cursor.close()
			connection.close()
