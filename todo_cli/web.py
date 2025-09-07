from __future__ import annotations

import argparse
import os
from typing import Optional

from flask import Flask, redirect, render_template, request, url_for

from .storage import TodoStorage


def create_app(db_path: Optional[str] = None) -> Flask:
	resolved_db = db_path or os.getenv("TODO_DB_PATH")
	storage = TodoStorage(db_path=resolved_db)
	app = Flask(
		__name__, template_folder="templates", static_folder="static"
	)

	@app.get("/")
	def index():
		filter_value = request.args.get("filter", "pending")
		if filter_value == "all":
			tasks = storage.list_tasks(include_completed=None)
		elif filter_value == "completed":
			tasks = storage.list_tasks(include_completed=True)
		else:
			tasks = storage.list_tasks(include_completed=False)
		return render_template("index.html", tasks=tasks, filter_value=filter_value)

	@app.post("/add")
	def add_task():
		title = (request.form.get("title") or "").strip()
		if title:
			storage.add_task(title)
		return redirect(url_for("index"))

	@app.post("/toggle/<int:task_id>")
	def toggle_task(task_id: int):
		task = storage.get_task(task_id)
		if task:
			storage.upsert_task(task.with_completed(not task.completed))
		return redirect(url_for("index", filter=request.args.get("filter")))

	@app.get("/edit/<int:task_id>")
	def edit_task_get(task_id: int):
		task = storage.get_task(task_id)
		if not task:
			return redirect(url_for("index"))
		return render_template("edit.html", task=task)

	@app.post("/edit/<int:task_id>")
	def edit_task_post(task_id: int):
		task = storage.get_task(task_id)
		if not task:
			return redirect(url_for("index"))
		title = (request.form.get("title") or "").strip()
		if title:
			storage.upsert_task(task.with_title(title))
		return redirect(url_for("index"))

	@app.post("/delete/<int:task_id>")
	def delete_task(task_id: int):
		storage.delete_task(task_id)
		return redirect(url_for("index"))

	return app


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(prog="todo-web", description="To-Do Web App")
	parser.add_argument("--db", type=str, default=None, help="Path to JSON db file")
	parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind")
	parser.add_argument("--port", type=int, default=8000, help="Port to bind")
	parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
	return parser


def run(argv: Optional[list[str]] = None) -> None:
	args = build_parser().parse_args(argv)
	app = create_app(db_path=args.db)
	app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
	run()

