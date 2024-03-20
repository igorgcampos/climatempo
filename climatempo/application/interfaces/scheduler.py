from abc import ABC, abstractmethod
from typing import Callable, Literal


class IScheduler(ABC):
    @abstractmethod
    def schedule(
        self,
        every: Literal["day", "minutes"],
        at: int | str,
        do: Callable[[], None],
        timezone: str | None,
    ) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
