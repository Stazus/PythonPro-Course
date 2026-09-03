from datetime import datetime
from pathlib import Path

log_dir = Path("/data")
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / "app.log"

with log_file.open("a", encoding="utf-8") as file:
    file.write(f"{datetime.now()} - Kontener został uruchomiony\n")

print("Log został zapisany do /data/app.log")
