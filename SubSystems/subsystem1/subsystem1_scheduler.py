import sys
import math
from SubSystems.subsystem1.subsystem1_task import subsystem1_task

def weighted_round_robbin(ready_queue: list, given_task: subsystem1_task) -> int:
    # if len(ready_queue) > 0:
    #     min_remaining_execution_time = given_task.get_remaining_execution_time()
    #     for task in ready_queue:
    #         min_remaining_execution_time = min(min_remaining_execution_time, given_task.get_remaining_execution_time())
    #     return int(math.ceil(given_task.get_remaining_execution_time() / min_remaining_execution_time))
    # else:
    #     return given_task.get_remaining_execution_time()
    return max(1, math.ceil(0.5 * given_task.get_remaining_execution_time()))