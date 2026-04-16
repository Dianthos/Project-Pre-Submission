"""Persistence layer (JSON file) for the Student Assignment Manager."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

from .manager import TaskManager


@dataclass
class JsonStorage:
    path: Path

    def load(self) -> TaskManager:
        if not self.path.exists():
            return TaskManager()
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("Data file is corrupted: expected a list")
        return TaskManager.from_list(data)

    def save(self, manager: TaskManager) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload: List[dict] = manager.to_list()
        self.path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
