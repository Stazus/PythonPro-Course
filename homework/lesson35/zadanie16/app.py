import random


HIGH_LOAD_THRESHOLD = 70
LOW_LOAD_THRESHOLD = 30
REQUIRED_MEASUREMENTS = 3
ITERATIONS = 20


def simulate_load():
    return random.randint(20, 90)


def run_simulation():
    high_load_count = 0
    low_load_count = 0
    action_history = []

    for iteration in range(1, ITERATIONS + 1):
        cpu_load = simulate_load()

        print(
            f"Pomiar {iteration:02d}: "
            f"obciążenie CPU = {cpu_load}%"
        )

        if cpu_load > HIGH_LOAD_THRESHOLD:
            high_load_count += 1
            low_load_count = 0

        elif cpu_load < LOW_LOAD_THRESHOLD:
            low_load_count += 1
            high_load_count = 0

        else:
            high_load_count = 0
            low_load_count = 0

        if high_load_count == REQUIRED_MEASUREMENTS:
            action = (
                f"Pomiar {iteration}: uruchomiono nową instancję "
                f"(CPU > {HIGH_LOAD_THRESHOLD}% przez "
                f"{REQUIRED_MEASUREMENTS} pomiary)"
            )

            print(f"AUTO-SCALING: {action}")
            action_history.append(action)
            high_load_count = 0

        elif low_load_count == REQUIRED_MEASUREMENTS:
            action = (
                f"Pomiar {iteration}: zatrzymano instancję "
                f"(CPU < {LOW_LOAD_THRESHOLD}% przez "
                f"{REQUIRED_MEASUREMENTS} pomiary)"
            )

            print(f"AUTO-SCALING: {action}")
            action_history.append(action)
            low_load_count = 0

    return action_history


if __name__ == "__main__":
    history = run_simulation()

    print("\nHistoria akcji:")

    if history:
        for action in history:
            print(f"- {action}")
    else:
        print("Brak akcji auto-scalingu.")
