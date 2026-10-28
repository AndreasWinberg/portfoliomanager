from datetime import date
from pathlib import Path
from xml.etree.ElementTree import iterparse
from zipfile import ZipFile as Zip

import httpx

FIRDS_URL = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select"
VALID_START = date(1950, 1, 1)
VALID_END = date(9999, 12, 31)
NS = "{urn:iso:std:iso:20022:tech:xsd:auth.017.001.02}"
EEA = {
    "AT",
    "BE",
    "BG",
    "CY",
    "CZ",
    "DE",
    "DK",
    "EE",
    "ES",
    "FI",
    "FR",
    "GR",
    "HR",
    "HU",
    "IE",
    "IT",
    "LT",
    "LU",
    "LV",
    "MT",
    "NL",
    "PL",
    "PT",
    "RO",
    "SE",
    "SI",
    "SK",
    "IS",
    "LI",
    "NO",
}


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


def _find_date(elem, path: str) -> date | None:
    elem_text = elem.find(path)
    if elem_text is None:
        return None
    elem_date = date.fromisoformat(elem_text.text[:10])
    if elem_date == VALID_END:
        return None
    return elem_date


def _wanted(record: dict) -> bool:
    return (
        record["cfi"].startswith("ES")
        and record["rel_venue"] == record["venue"]
        and record["isin"][:2] in EEA
    )


def _healthy(record: dict) -> bool:
    term = record["term_date"]
    first = record["first"]
    if term is None:
        return True
    if term < VALID_START:
        return False
    return first is None or term >= first


def read_shares(path: Path) -> tuple[list[dict], int]:

    shares = []
    invalid = 0

    with Zip(path) as archive:
        xml_file = archive.open(archive.namelist()[0])

        for _, elem in iterparse(xml_file, events=("end",)):
            if elem.tag != NS + "RefData":
                continue

            record = {
                "isin": elem.find(f"{NS}FinInstrmGnlAttrbts/{NS}Id").text,
                "country": elem.find(f"{NS}FinInstrmGnlAttrbts/{NS}Id").text[:2],
                "cfi": elem.find(f"{NS}FinInstrmGnlAttrbts/{NS}ClssfctnTp").text,
                "currency": elem.find(f"{NS}FinInstrmGnlAttrbts/{NS}NtnlCcy").text,
                "lei": elem.find(f"{NS}Issr").text,
                "venue": elem.find(f"{NS}TradgVnRltdAttrbts/{NS}Id").text,
                "term_date": _find_date(elem, f"{NS}TradgVnRltdAttrbts/{NS}TermntnDt"),
                "rel_venue": elem.find(f"{NS}TechAttrbts/{NS}RlvntTradgVn").text,
                "first": _find_date(elem, f"{NS}TradgVnRltdAttrbts/{NS}FrstTradDt"),
            }

            elem.clear()

            if not _wanted(record):
                continue

            if _healthy(record):
                shares.append(record)
                continue

            invalid += 1

    return shares, invalid
