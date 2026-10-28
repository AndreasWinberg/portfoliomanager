from datetime import date
from pathlib import Path

import httpx

FIRDS_URL = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select"


def list_files(start: date, end: date, rows: int = 1000) -> list[dict]:

    start_date = start.isoformat()
    end_date = end.isoformat()
    params = {
        "q": "*",
        "rows": rows,
        "wt": "json",
        "fq": f"publication_date:[{start_date}T00:00:00Z TO {end_date}T23:59:59Z]",
    }
    response = httpx.get(FIRDS_URL, params=params)
    response.raise_for_status()
    data = response.json()
    result = data["response"]
    if result["numFound"] > rows:
        raise ValueError(f"{result['numFound']} rows found, {rows} requested.")
    return result["docs"]


def download(link: str, folder: Path) -> Path:
    folder.mkdir(exist_ok=True)
    file_name = link.split("/")[-1]
    file_path = folder / file_name
    response = httpx.get(link)
    response.raise_for_status()
    file_path.write_bytes(response.content)
    return file_path
