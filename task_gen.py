import secrets
import json
from datetime import datetime, timedelta

COLOR_NAMES = [
    "red",
    "green",
    "blue",
    "yellow",
    "orange",
    "purple",
    "pink",
    "brown",
    "cyan",
]

def secure_sample(population, k):
    """
    Select k unique elements from 'population' using only 'secrets'-based randomness.
    This is similar to random.sample() but uses secrets for cryptographic security.
    """
    if k > len(population):
        raise ValueError("Sample size cannot exceed the size of the population")
    population_copy = list(population)
    selected = []
    for _ in range(k):
        index = secrets.randbelow(len(population_copy))
        selected.append(population_copy.pop(index))
    return selected

def generate_task_json(
    filename="task.json",
    task_id="task-0001",
    width=800,
    height=600,
    circle_count=12,
    circle_radius=20,
    highlight_count=3,
    task_instructions="Click the highlighted circles",
    expiration_minutes=5
):
    circle_data = []
    for i in range(circle_count):
        circle_id = f"circle-{i}"
        x = secrets.randbelow(width - 2 * circle_radius) + circle_radius
        y = secrets.randbelow(height - 2 * circle_radius) + circle_radius
        color = secrets.choice(COLOR_NAMES)
        circle_data.append({
            "id": circle_id,
            "x": x,
            "y": y,
            "color": color
        })

    if highlight_count > circle_count:
        highlight_count = circle_count

    selected_circles = secure_sample(circle_data, highlight_count)
    target_ids = [c["id"] for c in selected_circles]

    creation_date = datetime.utcnow()
    expiration_date = creation_date + timedelta(minutes=expiration_minutes)

    data = {
        "taskId": task_id,
        "circles": circle_data,
        "creationDate": creation_date.isoformat(),
        "task": task_instructions,
        "expirationDate": expiration_date.isoformat(),
        "expectedResponse": target_ids
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    generate_task_json(filename="sample_task_with_named_colors.json", task_id="task-1234")
    print("Task JSON file generated.")