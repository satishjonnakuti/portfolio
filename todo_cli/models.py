from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass
class Task:
	id: int
	title: str
	completed: bool
	created_at: str
	updated_at: str

	@staticmethod
	def create(task_id: int, title: str) -> "Task":
		now = datetime.now(timezone.utc).isoformat()
		return Task(
			id=task_id,
			title=title,
			completed=False,
			created_at=now,
			updated_at=now,
		)

	@staticmethod
	def from_dict(data: Dict[str, Any]) -> "Task":
		return Task(
			id=int(data["id"]),
			title=str(data["title"]),
			completed=bool(data.get("completed", False)),
			created_at=str(data.get("created_at") or data.get("createdAt")),
			updated_at=str(
				data.get("updated_at")
				or data.get("updatedAt")
				or data.get("created_at")
			),
		)

	def to_dict(self) -> Dict[str, Any]:
		return asdict(self)

	def with_title(self, new_title: str) -> "Task":
		now = datetime.now(timezone.utc).isoformat()
		return Task(
			id=self.id,
			title=new_title,
			completed=self.completed,
			created_at=self.created_at,
			updated_at=now,
		)

	def with_completed(self, is_completed: bool) -> "Task":
		now = datetime.now(timezone.utc).isoformat()
		return Task(
			id=self.id,
			title=self.title,
			completed=is_completed,
			created_at=self.created_at,
			updated_at=now,
		)

