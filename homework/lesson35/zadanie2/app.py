import shutil
from datetime import datetime
from pathlib import Path


source_directory = Path("zadanie1")
backup_directory = Path("backups")

backup_directory.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_name = f"backup_{timestamp}"
backup_path = backup_directory / backup_name

try:
    shutil.copytree(source_directory, backup_path)

    print("Kopia zapasowa została utworzona pomyślnie.")
    print(f"Źródło: {source_directory}")
    print(f"Backup: {backup_path}")

except Exception as error:
    print(f"Błąd podczas tworzenia kopii zapasowej: {error}")
