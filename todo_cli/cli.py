import argparse
from typing import Optional

from .models import Task
from .storage import TodoStorage


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(prog="todo", description="Simple To-Do List CLI")
	parser.add_argument("--db", type=str, default=None, help="Path to the JSON database file")
	subparsers = parser.add_subparsers(dest="command", required=True)

	# add
	p_add = subparsers.add_parser("add", help="Add a new task")
	p_add.add_argument("title", type=str, help="Task title")

	# list
	p_list = subparsers.add_parser("list", help="List tasks")
	group = p_list.add_mutually_exclusive_group()
	group.add_argument("-a", "--all", action="store_true", help="Show all tasks")
	group.add_argument("-c", "--completed", action="store_true", help="Show only completed tasks")
	group.add_argument("-p", "--pending", action="store_true", help="Show only pending tasks")
	p_list.add_argument("--raw", action="store_true", help="Raw output without header")

	# done
	p_done = subparsers.add_parser("done", help="Mark a task as completed")
	p_done.add_argument("id", type=int, help="Task id")

	# undone
	p_undone = subparsers.add_parser("undone", help="Mark a task as not completed")
	p_undone.add_argument("id", type=int, help="Task id")

	# delete
	p_delete = subparsers.add_parser("delete", help="Delete a task")
	p_delete.add_argument("id", type=int, help="Task id")

	# edit
	p_edit = subparsers.add_parser("edit", help="Edit a task's title")
	p_edit.add_argument("id", type=int, help="Task id")
	p_edit.add_argument("title", type=str, help="New title")

	return parser


def _print_tasks(tasks, raw: bool) -> None:
	if not raw:
		print("ID  Status  Title")
		print("--  ------  -----")
	for t in tasks:
		status = "x" if t.completed else " "
		print(f"{t.id:<3}[{status}]    {t.title}")


def main(argv: Optional[list[str]] = None) -> None:
	parser = build_parser()
	args = parser.parse_args(argv)
	storage = TodoStorage(db_path=args.db)

	if args.command == "add":
		task = storage.add_task(args.title)
		print(f"Added #{task.id}: {task.title}")
		return

	if args.command == "list":
		if args.all:
			include_completed = None
		elif args.completed:
			include_completed = True
		elif args.pending:
			include_completed = False
		else:
			include_completed = False
		tasks = storage.list_tasks(include_completed=include_completed)
		_previous_raw = args.raw
		_print_tasks(tasks, raw=_previous_raw)
		return

	if args.command == "done":
		task = storage.get_task(args.id)
		if not task:
			print(f"Task #{args.id} not found")
			raise SystemExit(1)
		storage.upsert_task(task.with_completed(True))
		print(f"Marked #{args.id} as completed")
		return

	if args.command == "undone":
		task = storage.get_task(args.id)
		if not task:
			print(f"Task #{args.id} not found")
			raise SystemExit(1)
		storage.upsert_task(task.with_completed(False))
		print(f"Marked #{args.id} as not completed")
		return

	if args.command == "delete":
		ok = storage.delete_task(args.id)
		if not ok:
			print(f"Task #{args.id} not found")
			raise SystemExit(1)
		print(f"Deleted #{args.id}")
		return

	if args.command == "edit":
		task = storage.get_task(args.id)
		if not task:
			print(f"Task #{args.id} not found")
			raise SystemExit(1)
		storage.upsert_task(task.with_title(args.title))
		print(f"Edited #{args.id}")
		return

