import time
from typing import Any, Callable, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed


def execute_in_paralelal(
    executables: List[Tuple[Callable[[Any], Any], Any]],
    max_workers: int = 10,
    get_callback: bool = True,
) -> Any | None:
    futures = []
    future_results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(*execute) for execute in executables]
    if get_callback:
        for future in as_completed(futures):
            future_results.append(future.result())
        return future_results
    return None


def execution_flow(
    interval_in_seconds: int,
    execution_after_interval: int,
    executables: List[Tuple[Callable[[Any], Any], Any]],
):
    callback = []
    while executables:
        callback += execute_in_paralelal(
            executables=executables[:execution_after_interval],
            max_workers=execution_after_interval,
        )
        del executables[:execution_after_interval]
        if executables:
            time.sleep(interval_in_seconds)
    return callback


def execute_on_interval(
    interval_in_seconds: int,
    to_execute_in_interval: int,
    executables: List[Tuple[Callable[[Any], Any], Any]],
):
    if to_execute_in_interval <= 1:
        raise AttributeError("You must to execute more than one executable per second")
    futures = []
    while executables:
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures.extend(
                [
                    executor.submit(*execute)
                    for execute in executables[:to_execute_in_interval]
                ]
            )
            del executables[:to_execute_in_interval]
        time.sleep(interval_in_seconds)
    return [future.result() for future in as_completed(futures)]
