from typing import List
from abc import ABC, abstractmethod


class Handler(ABC):
    @abstractmethod
    def execute(self, event_data: List[dict]) -> None:
        pass
