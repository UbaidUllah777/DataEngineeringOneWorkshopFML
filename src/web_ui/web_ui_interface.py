from collections.abc import Callable, Iterable
from html import escape
from typing import Any


class WebUIInterface:
	"""Framework-neutral web UI service for displaying database records."""

	def __init__(
		self,
		title: str = "Data Engineering Dashboard",
		data_loader: Callable[[], Iterable[dict[str, Any]]] | None = None,
	) -> None:
		self.title = title
		self.data_loader = data_loader
		self.records: list[dict[str, Any]] = []

	def load_data(self) -> list[dict[str, Any]]:
		"""Load records from the configured data source."""
		# TODO: Connect this callback to DatabaseServiceAgent.fetch_records().
		if self.data_loader is None:
			return self.records

		self.records = [dict(record) for record in self.data_loader()]
		return self.records

	def filter_records(self, search_text: str = "") -> list[dict[str, Any]]:
		"""Return records containing the search text in any field."""
		search_text = search_text.strip().lower()
		if not search_text:
			return self.records

		return [
			record
			for record in self.records
			if any(search_text in str(value).lower() for value in record.values())
		]

	def render_table(self, records: Iterable[dict[str, Any]] | None = None) -> str:
		"""Render records as a basic HTML table."""
		rows = list(self.records if records is None else records)
		if not rows:
			return "<p>No records found.</p>"

		columns = list(rows[0])
		header = "".join(f"<th>{escape(str(column))}</th>" for column in columns)
		body = "".join(
			"<tr>"
			+ "".join(f"<td>{escape(str(record.get(column, '')))}</td>" for column in columns)
			+ "</tr>"
			for record in rows
		)
		return f"<table><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table>"

	def render_page(self, search_text: str = "") -> str:
		"""Render the complete page shown to a browser."""
		filtered_records = self.filter_records(search_text)
		return (
			"<!DOCTYPE html>"
			"<html><head>"
			f"<title>{escape(self.title)}</title>"
			"</head><body>"
			f"<h1>{escape(self.title)}</h1>"
			f"{self.render_table(filtered_records)}"
			"</body></html>"
		)

	def run(self) -> None:
		"""Start the web application."""
		# TODO: Add the chosen web framework and register render_page() as a route.
		raise NotImplementedError("Web server startup is not configured yet")