from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import Task


class TodoStorage:
	def __init__(self, db_path: Optional[str] = None) -> None:
		self.path = Path(db_path) if db_path else self.default_db_path()
		self._ensure_file()

	@staticmethod
	def default_db_path() -> Path:
		from os import getenv
		xdg = getenv("XDG_DATA_HOME")
		if xdg:
			base = Path(xdg) / "todo_cli"
		else:
			base = Path.home() / ".todo_cli"
		base.mkdir(parents=True, exist_ok=True)
		return base / "todos.json"

	def _ensure_file(self) -> None:
		if not self.path.exists():
			self.path.parent.mkdir(parents=True, exist_ok=True)
			data = {"next_id": 1, "tasks": []}
			self.path.write_text(json.dumps(data, indent=2))

	def _read_data(self) -> Dict[str, Any]:
		try:
			raw = self.path.read_text()
			if not raw.strip():
				return {"next_id": 1, "tasks": []}
			return json.loads(raw)
		except json.JSONDecodeError:
			# If the file is corrupted, reset to empty structure
			return {"next_id": 1, "tasks": []}

	def _write_data(self, data: Dict[str, Any]) -> None:
		self.path.write_text(json.dumps(data, indent=2))

	def list_tasks(self, include_completed: Optional[bool] = None) -> List[Task]:
		data = self._read_data()
		tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
		if include_completed is None:
			return tasks
		if include_completed:
			return [t for t in tasks if t.completed]
		return [t for t in tasks if not t.completed]

	def add_task(self, title: str) -> Task:
		data = self._read_data()
		next_id = int(data.get("next_id", 1))
		task = Task.create(next_id, title)
		tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
		tasks.append(task)
		data["tasks"] = [t.to_dict() for t in tasks]
		data["next_id"] = next_id + 1
		self._write_data(data)
		return task

	def get_task(self, task_id: int) -> Optional[Task]:
		data = self._read_data()
		for t in data.get("tasks", []):
			if int(t["id"]) == int(task_id):
				return Task.from_dict(t)
		return None

	def upsert_task(self, task: Task) -> None:
		data = self._read_data()
		tasks = data.get("tasks", [])
		replaced = False
		for idx, t in enumerate(tasks):
			if int(t["id"]) == task.id:
				tasks[idx] = task.to_dict()
				replaced = True
				break
		if not replaced:
			tasks.append(task.to_dict())
		data["tasks"] = tasks
		self._write_data(data)

	def delete_task(self, task_id: int) -> bool:
		data = self._read_data()
		tasks = data.get("tasks", [])
		new_tasks = [t for t in tasks if int(t["id"]) != int(task_id)]
		if len(new_tasks) == len(tasks):
			return False
		data["tasks"] = new_tasks
		self._write_data(data)
		return True

