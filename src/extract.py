import requests
import zipfile
import pandas as pd
from io import BytesIO
from pathlib import Path

BKK_GTFS_URL = "https://bkk.hu/gtfs/budapest_gtfs.zip"
FILES_TO_EXTRACT = ("stops.txt", "routes.txt", "trips.txt", "stop_times.txt", "calendar_dates.txt")
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

def extract(link: str=BKK_GTFS_URL, files_to_extract: tuple[str]=FILES_TO_EXTRACT): 
    try:
        response = requests.get(link)
    except requests.RequestException as e:
        print(f"Error occurred while fetching data: {e}")
        return

    response.raise_for_status()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    zip_bytes = BytesIO(response.content)
    with zipfile.ZipFile(zip_bytes, "r") as zfile:
        for file in files_to_extract:
            try:
                zfile.getinfo(file)
            except KeyError:
                print(f"File {file} not found in the zip archive.")
                continue
            with zfile.open(file) as f:
                df = pd.read_csv(f)
            df.to_csv(DATA_DIR / f"{Path(file).stem}.csv", index=False, encoding="utf-8")

if __name__ == "__main__":
    extract()