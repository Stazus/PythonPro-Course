from pathlib import Path


def parse_log(file_path):
    log_counts = {
        "ERROR": 0,
        "WARNING": 0,
        "INFO": 0,
    }

    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            for level in log_counts:
                if f"{level}:" in line:
                    log_counts[level] += 1

    return log_counts


if __name__ == "__main__":
    result = parse_log("zadanie7/app.log")
    print(result)
