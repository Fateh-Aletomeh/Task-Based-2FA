import random
import json
from datetime import datetime, timedelta

COLOR_NAMES = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "brown", "cyan", "magenta"]

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
        x = random.randint(circle_radius, width - circle_radius)
        y = random.randint(circle_radius, height - circle_radius)
        color = random.choice(COLOR_NAMES)
        circle_data.append({
            "id": circle_id,
            "x": x,
            "y": y,
            "color": color
        })
    if highlight_count > circle_count:
        highlight_count = circle_count
    selected_circles = random.sample(circle_data, highlight_count)
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
