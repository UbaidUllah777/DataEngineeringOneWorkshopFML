import os
from collections.abc import Sequence
from typing import Any

import psycopg
from psycopg.rows import dict_row
from psycopg.sql import Identifier, SQL


class DatabaseServiceAgent:
	"""Small PostgreSQL service for a Neon database."""

	def __init__(self, connection_string: str | None = None) -> None:
		self.connection_string = connection_string or os.getenv("DATABASE_URL")
		self.connection: psycopg.Connection[Any] | None = None

	def connect(self) -> None:
		"""Open a connection to Neon using the PostgreSQL connection URL."""
		if not self.connection_string:
			raise ValueError("DATABASE_URL is not configured")

		# TODO: Add Neon-specific pool configuration when concurrent access is needed.
		self.connection = psycopg.connect(
			self.connection_string,
			row_factory=dict_row,
		)

	def execute_query(
		self,
		query: str,
		parameters: Sequence[Any] | None = None,
	) -> list[dict[str, Any]]:
		"""Execute a parameterized query and return rows for read queries."""
		connection = self._require_connection()

		try:
			with connection.cursor() as cursor:
				cursor.execute(query, parameters)
				rows = cursor.fetchall() if cursor.description else []
			connection.commit()
			return [dict(row) for row in rows]
		except Exception:
			connection.rollback()
			raise

	def insert_record(self, table_name: str, record: dict[str, Any]) -> None:
		"""Insert one record into a Neon/PostgreSQL table."""
		if not record:
			raise ValueError("record must contain at least one field")

		columns = list(record)
		query = SQL("INSERT INTO {} ({}) VALUES ({})").format(
			Identifier(table_name),
			SQL(", ").join(Identifier(column) for column in columns),
			SQL(", ").join(SQL("%s") for _ in columns),
		)
		self.execute_query(query.as_string(self._require_connection()), tuple(record.values()))

	def fetch_records(self, table_name: str) -> list[dict[str, Any]]:
		"""Fetch all records from a Neon/PostgreSQL table."""
		query = SQL("SELECT * FROM {}").format(Identifier(table_name))
		return self.execute_query(query.as_string(self._require_connection()))

	def close(self) -> None:
		"""Close the Neon database connection if it is open."""
		if self.connection is not None:
			self.connection.close()
			self.connection = None

	def _require_connection(self) -> psycopg.Connection[Any]:
		if self.connection is None or self.connection.closed:
			raise RuntimeError("Database is not connected")
		return self.connection
class DatabaseServiceAgent:
	"""Dummy database service for the workshop project."""

	def __init__(self, connection_string: str) -> None:
		self.connection_string = connection_string
		self.is_connected = False

	def connect(self) -> None:
		"""Open a database connection."""
		# TODO: Create a real database connection here.
		self.is_connected = True

	def execute_query(self, query: str) -> list[dict[str, str]]:
		"""Execute a query and return dummy rows."""
		# TODO: Validate the query and execute it using the database client.
		if not self.is_connected:
			raise RuntimeError("Database is not connected")

		return [{"query": query}]

	def insert_record(self, table_name: str, record: dict[str, str]) -> None:
		"""Insert one record into a database table."""
		# TODO: Use a parameterized INSERT statement to save the record.
		if not self.is_connected:
			raise RuntimeError("Database is not connected")

	def fetch_records(self, table_name: str) -> list[dict[str, str]]:
		"""Fetch records from a database table."""
		# TODO: Replace this placeholder with a SELECT query.
		if not self.is_connected:
			raise RuntimeError("Database is not connected")

		return [{"table": table_name}]

	def close(self) -> None:
		"""Close the database connection."""
		# TODO: Close the real database client when one is configured.
		self.is_connected = False
