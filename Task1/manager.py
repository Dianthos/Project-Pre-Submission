"""TaskManager: core business logic for the app."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, Iterable, List, Optional

from .models import Task


@dataclass
class TaskManager:
    """Manages a collection of Task objects.

    Encapsulation notes:
    - tasks are stored internally in a dict keyed by task_id
    - external code interacts via methods (add/delete/mark/search/sort)
    """

    _tasks: Dict[int, Task] = field(default_factory=dict)
    _next_id: int = 1

    @property
    def size(self) -> int:
        return len(self._tasks)

    def all_tasks(self) -> List[Task]:
        return sorted(self._tasks.values(), key=lambda t: (t.due_date, t.course.lower(), t.title.lower()))

    def sort_by_due_date(self, descending: bool = False) -> List[Task]:
        """Return tasks sorted by due date.

        This is a convenience wrapper for presentation/demo.
        """
        tasks = self.all_tasks()
        return list(reversed(tasks)) if descending else tasks

    def get(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def add(self, task: Task) -> Task:
        # Ensure unique id
        if task.task_id <= 0:
            task.task_id = self._next_id
        if task.task_id in self._tasks:
            raise ValueError(f"Task id {task.task_id} already exists")
        self._tasks[task.task_id] = task
        self._next_id = max(self._next_id, task.task_id + 1)
        return task

    def create_and_add(self, task_cls, **kwargs) -> Task:
        task = task_cls(task_id=self._next_id, **kwargs)
        return self.add(task)

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None

    def mark_completed(self, task_id: int, completed: bool = True) -> bool:
        task = self._tasks.get(task_id)
        if not task:
            return False
        task.completed = completed
        return True

    def update_title(self, task_id: int, new_title: str) -> bool:
        task = self._tasks.get(task_id)
        if not task:
            return False
        task.title = new_title.strip()
        return True

    def search(self, keyword: str) -> List[Task]:
        kw = keyword.strip().lower()
        if not kw:
            return []
        return [t for t in self.all_tasks() if kw in t.title.lower() or kw in t.course.lower()]

    def by_course(self, course: str) -> List[Task]:
        c = course.strip().lower()
        return [t for t in self.all_tasks() if t.course.lower() == c]

    def due_before(self, d: date) -> List[Task]:
        return [t for t in self.all_tasks() if t.due_date <= d]

    def load_many(self, tasks: Iterable[Task]) -> None:
        for t in tasks:
            self.add(t)

    def to_list(self) -> List[dict]:
        return [t.to_dict() for t in self.all_tasks()]

    @classmethod
    def from_list(cls, items: List[dict]) -> "TaskManager":
        mgr = cls()
        for d in items:
            mgr.add(Task.from_dict(d))
        return mgr

    def next_id(self) -> int:
        return self._next_id

    def filter_by_course(self, course: str):
        return self.by_course(course)

    def remove(self, task_id: int) -> bool:
        return self.delete(task_id)

