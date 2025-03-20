import json
import secrets
from datetime import datetime, timedelta

COLOR_NAMES = [
    "red", "green", "blue", "yellow", "orange", 
    "purple", "pink"
]

def secure_sample(population, k):
    if k > len(population):
        raise ValueError("Sample size cannot exceed the size of the population")
    population_copy = list(population)
    selected = []
    for _ in range(k):
        index = secrets.randbelow(len(population_copy))
        selected.append(population_copy.pop(index))
    return selected

def generate_json_file(
    filename="sample_task.json",
    task_id="task-5678",
    circle_count=16,
    expiration_minutes=5
):
    circles = []
    for i in range(circle_count):
        circle_id = f"circle-{i}"
        # Choose a random color name using secrets
        color = secrets.choice(COLOR_NAMES)
        circles.append({"id": circle_id, "color": color})

    # Decide how many circles to select as the "expectedResponse"
    # For example, let's pick between 1 and 5 randomly:
    highlight_count = secrets.randbelow(5) + 1
    if highlight_count > circle_count:
        highlight_count = circle_count

    selected = secure_sample(circles, highlight_count)
    expected_response = [c["id"] for c in selected]

    creation_time = datetime.utcnow()
    expiration_time = creation_time + timedelta(minutes=expiration_minutes)

    data = {
        "taskId": task_id,
        "circles": circles,
        "creationDate": creation_time.isoformat(),
        "expirationDate": expiration_time.isoformat(),
        "expectedResponse": expected_response
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    generate_json_file()
    print("Sample JSON file generated successfully.")
