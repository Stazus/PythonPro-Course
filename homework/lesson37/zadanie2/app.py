import os

name = os.getenv("NAME", "Docker")
print(f"Hello, {name}!")
