"""Task models for the Student Assignment Manager.

Design goals:
- Clear OOP structure (base class + subclasses)
- Easy (de)serialization for saving to JSON
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, Type


def parse_date(value: str) -> date:
    """Parse YYYY-MM-DD into a date."""
    return datetime.strptime(value, "%Y-%m-%d").date()


@dataclass
class Task(ABC):
    """Abstract base class for all tasks."""

    task_id: int
    title: str
    course: str
    due_date: date
    completed: bool = False

    def mark_done(self) -> None:
        self.completed = True

    def mark_todo(self) -> None:
        self.completed = False

    @property
    def status(self) -> str:
        return "DONE" if self.completed else "TODO"

    @abstractmethod
    def kind(self) -> str:
        """A short type label for display and serialization."""

    @abstractmethod
    def details(self) -> str:
        """Extra details shown in list view."""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.kind(),
            "task_id": self.task_id,
            "title": self.title,
            "course": self.course,
            "due_date": self.due_date.isoformat(),
            "completed": self.completed,
            **self._extra_dict(),
        }

    def _extra_dict(self) -> Dict[str, Any]:
        return {}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        task_type = data.get("type")
        cls_map: Dict[str, Type[Task]] = {
            "assignment": AssignmentTask,
            "exam": ExamTask,
            "general": GeneralTask,
        }
        if task_type not in cls_map:
            raise ValueError(f"Unknown task type: {task_type}")
        return cls_map[task_type]._from_dict(data)


@dataclass
class AssignmentTask(Task):
    weight_percent: float = 0.0

    def kind(self) -> str:
        return "assignment"

    def details(self) -> str:
        w = f"{self.weight_percent:g}%" if self.weight_percent else "-"
        return f"weight={w}"

    def _extra_dict(self) -> Dict[str, Any]:
        return {"weight_percent": self.weight_percent}

    @staticmethod
    def _from_dict(data: Dict[str, Any]) -> "AssignmentTask":
        return AssignmentTask(
            task_id=int(data["task_id"]),
            title=str(data["title"]),
            course=str(data["course"]),
            due_date=parse_date(str(data["due_date"])),
            completed=bool(data.get("completed", False)),
            weight_percent=float(data.get("weight_percent", 0.0)),
        )


@dataclass
class ExamTask(Task):
    location: str = "TBD"

    def kind(self) -> str:
        return "exam"

    def details(self) -> str:
        return f"location={self.location}"

    def _extra_dict(self) -> Dict[str, Any]:
        return {"location": self.location}

    @staticmethod
    def _from_dict(data: Dict[str, Any]) -> "ExamTask":
        return ExamTask(
            task_id=int(data["task_id"]),
            title=str(data["title"]),
            course=str(data["course"]),
            due_date=parse_date(str(data["due_date"])),
            completed=bool(data.get("completed", False)),
            location=str(data.get("location", "TBD")),
        )


@dataclass
class GeneralTask(Task):
    note: str = ""

    def kind(self) -> str:
        return "general"

    def details(self) -> str:
        return f"note={self.note[:24] + ('…' if len(self.note) > 24 else '')}" if self.note else "-"

    def _extra_dict(self) -> Dict[str, Any]:
        return {"note": self.note}

    @staticmethod
    def _from_dict(data: Dict[str, Any]) -> "GeneralTask":
        return GeneralTask(
            task_id=int(data["task_id"]),
            title=str(data["title"]),
            course=str(data["course"]),
            due_date=parse_date(str(data["due_date"])),
            completed=bool(data.get("completed", False)),
            note=str(data.get("note", "")),
        )
