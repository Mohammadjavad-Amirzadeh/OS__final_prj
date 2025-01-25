import json
from datetime import datetime

class ExecutionTracker:
    def __init__(self):
        self.tasks = {}
        
    def add_task(self, task_name, arrival_time, subsystem):
        self.tasks[task_name] = {
            "subsystem": subsystem,
            "arrival_time": arrival_time,
            "finish_time": None,
            "total_execution_time": 0,  # For periodic tasks, this will be cumulative
            "completed_by_core": None  # Add field for tracking which core completed the task
        }
    
    def task_finished(self, task_name, finish_time, total_execution_time, core_name):  # Add core_name parameter
        if task_name in self.tasks:
            self.tasks[task_name]["finish_time"] = finish_time
            self.tasks[task_name]["total_execution_time"] = total_execution_time
            self.tasks[task_name]["completed_by_core"] = core_name  # Record which core completed it
            self.tasks[task_name]["waiting_time"] = (
                finish_time - 
                self.tasks[task_name]["arrival_time"] - 
                total_execution_time + 
                1  # Add 1 to include arrival time unit
            )
    
    def save_report(self):
        report = {
            "tasks": self.tasks,
            "metadata": {
                "generation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_tasks": len(self.tasks)
            }
        }
        
        with open("execution_report.json", 'w') as f:
            json.dump(report, f, indent=4)
