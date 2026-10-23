from datetime import date

import httpx


def list_files(start: date, end: date, rows: int = 1000) -> list[dict]:
    url = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select"
    start_date = start.isoformat()
    end_date = end.isoformat()
    params = {
        "q": "*",
        "rows": rows,
        "wt": "json",
        "fq": f"publication_date:[{start_date}T00:00:00Z TO {end_date}T23:59:59Z]",
    }
    response = httpx.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    result = data["response"]
    if result["numFound"] > rows:
        raise ValueError(f"{result['numFound']} rowsfound, {rows} requested.")
    return result["docs"]
