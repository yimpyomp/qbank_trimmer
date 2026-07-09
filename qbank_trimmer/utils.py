from datetime import datetime
from pathlib import Path


def create_output_directory(base_directory):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    output_directory = base_directory / timestamp

    output_directory.mkdir(parents=True, exist_ok=False)

    return output_directory