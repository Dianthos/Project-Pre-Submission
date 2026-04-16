"""Student Assignment Manager (Task 1)

CLI app designed to demonstrate:
- modular programming (multiple modules/files)
- OOP concepts: encapsulation, inheritance, polymorphism, abstraction

Run:
  python -m task1.main
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

from .manager import TaskManager
from .models import AssignmentTask, ExamTask, GeneralTask, parse_date
from .storage import JsonStorage


DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"


def prompt(msg: str) -> str:
    return input(msg).strip()


def prompt_date(msg: str, default: Optional[date] = None) -> date:
    while True:
        raw = prompt(msg + (f" [{default.isoformat()}]" if default else "") + ": ")
        if not raw and default:
            return default
        try:
            return parse_date(raw)
        except Exception:
            print("  ❌ Please enter a date in YYYY-MM-DD format.")


def prompt_bool(msg: str, default: bool = False) -> bool:
    suffix = "Y/n" if default else "y/N"
    raw = prompt(f"{msg} ({suffix}): ").lower()
    if not raw:
        return default
    return raw in {"y", "yes"}


def print_task_table(mgr: TaskManager) -> None:
    tasks = mgr.all_tasks()
    if not tasks:
        print("(No tasks yet)")
        return

    print("\nID  | Done | Due        | Course        | Kind       | Title (details)")
    print("----+------+------------+--------------+------------+------------------------------")
    for t in tasks:
        done = "✅" if t.completed else "  "
        course = (t.course[:12] + "…") if len(t.course) > 13 else t.course.ljust(13)
        kind = t.kind().ljust(10)
        title = (t.title[:18] + "…") if len(t.title) > 19 else t.title.ljust(19)
        print(f"{t.task_id:<3} |  {done}  | {t.due_date.isoformat()} | {course} | {kind} | {title} ({t.details()})")
    print()


def add_task_flow(mgr: TaskManager) -> None:
    print("\nAdd a task")
    print("1) Assignment  2) Exam  3) General")
    choice = prompt("> ")

    title = prompt("Title: ")
    course = prompt("Course (e.g., COMP2090): ")
    due = prompt_date("Due date (YYYY-MM-DD)")

    if choice == "1":
        points = prompt("Points (optional): ")
        t = AssignmentTask(
            task_id=mgr.next_id(),
            title=title,
            course=course,
            due_date=due,
            weight_percent=int(points) if points.isdigit() else None,
        )
    elif choice == "2":
        location = prompt("Location (optional): ")
        t = ExamTask(
            task_id=mgr.next_id(),
            title=title,
            course=course,
            due_date=due,
            location=location or "TBD",
        )
    else:
        note = prompt("Note (optional): ")
        t = GeneralTask(
            task_id=mgr.next_id(),
            title=title,
            course=course,
            due_date=due,
            note=note,
        )

    mgr.add(t)
    print("✅ Added.")


def mark_done_flow(mgr: TaskManager) -> None:
    try:
        task_id = int(prompt("Task ID to toggle complete: "))
    except ValueError:
        print("❌ Invalid ID")
        return
    t = mgr.get(task_id)
    if not t:
        print("❌ Not found")
        return
    mgr.mark_completed(task_id, not t.completed)
    print("✅ Updated.")


def delete_flow(mgr: TaskManager) -> None:
    try:
        task_id = int(prompt("Task ID to delete: "))
    except ValueError:
        print("❌ Invalid ID")
        return
    if not mgr.get(task_id):
        print("❌ Not found")
        return
    if prompt_bool("Are you sure?", default=False):
        mgr.remove(task_id)
        print("✅ Deleted.")


def search_flow(mgr: TaskManager) -> None:
    keyword = prompt("Keyword (title/course): ")
    results = mgr.search(keyword)
    if not results:
        print("(No matches)")
        return
    print("\nMatches:")
    for t in results:
        print(f"- [{t.task_id}] {t.title} ({t.course}) due {t.due_date.isoformat()}")


def filter_course_flow(mgr: TaskManager) -> None:
    course = prompt("Course code/name: ")
    results = mgr.filter_by_course(course)
    if not results:
        print("(No matches)")
        return
    print("\nTasks for course:")
    for t in results:
        print(f"- [{t.task_id}] {t.title} due {t.due_date.isoformat()} {'(done)' if t.completed else ''}")


def sort_flow(mgr: TaskManager) -> None:
    mgr.sort_by_due_date()
    print("✅ Sorted by due date.")


def load_manager() -> TaskManager:
    return JsonStorage(DATA_FILE).load()


def save_manager(mgr: TaskManager) -> None:
    JsonStorage(DATA_FILE).save(mgr)


def main() -> None:
    print("=== Student Assignment Manager ===")
    mgr = load_manager()

    while True:
        print("\nMenu")
        print("1) View all tasks")
        print("2) Add a task")
        print("3) Search")
        print("4) Filter by course")
        print("5) Sort by due date")
        print("6) Toggle done")
        print("7) Delete task")
        print("8) Save & exit")

        choice = prompt("> ")

        if choice == "1":
            print_task_table(mgr)
        elif choice == "2":
            add_task_flow(mgr)
        elif choice == "3":
            search_flow(mgr)
        elif choice == "4":
            filter_course_flow(mgr)
        elif choice == "5":
            sort_flow(mgr)
        elif choice == "6":
            mark_done_flow(mgr)
        elif choice == "7":
            delete_flow(mgr)
        elif choice == "8":
            save_manager(mgr)
            print("✅ Saved. Bye!")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()
