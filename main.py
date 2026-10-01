from dataclasses import asdict

from fastapi import FastAPI, HTTPException

from models import Task
from schemas import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI()

# In-memory storage: task_id -> Task
dataset: dict[int, Task] = {}


@app.post("/tasks", response_model=TaskResponse)
def create_task(task_data: TaskCreate):
    # Pydantic model -> dictionary
    data = task_data.model_dump()


    task_id = len(dataset) + 1

    # Dictionary -> dataclass
    new_task = Task(task_id=task_id, **data)
    dataset[task_id] = new_task

    # Dataclass -> dictionary -> response model
    return TaskResponse(**asdict(new_task))


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    tasks = []
    for task in dataset.values():
        task_dict = asdict(task)
        tasks.append(TaskResponse(**task_dict))
    return tasks


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in dataset:
        raise HTTPException(status_code=404, detail="Task not found")

    del dataset[task_id]
    return {"message": f"Task {task_id} deleted successfully"}


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    if task_id not in dataset:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only the fields the user actually sent
    update_data = task_update.model_dump(exclude_unset=True)

    # Get the old task and turn it into a dictionary
    old_task = dataset[task_id]
    task_dict = asdict(old_task)

    # Merge: new values overwrite old ones
    task_dict.update(update_data)

    # Build a brand new Task (the old one is frozen, we can't change it)
    new_task = Task(**task_dict)
    dataset[task_id] = new_task

    return TaskResponse(**asdict(new_task))