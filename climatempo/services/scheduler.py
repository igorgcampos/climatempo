import time
import schedule
from typing import Callable, Literal
from climatempo.application.interfaces.scheduler import IScheduler


class Scheduler(IScheduler):
    def schedule(
        self,
        every: Literal["day", "minutes"],
        at: int | str,
        do: Callable[[], None],
        timezone: str | None = None,
    ) -> None:
        match every:
            case "day":
                schedule.every().day.at(at, timezone).do(do)
            case "minutes":
                schedule.every(at).minutes.do(do)

    def run(self) -> None:
        while True:
            schedule.run_pending()
            time.sleep(1)
