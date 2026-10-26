"""Fetch cs.CV abstracts under CC BY 4.0 or CC BY-SA 4.0 from arXiv's OAI-PMH endpoint.

Usage: uv run python scripts/fetch_arxiv.py FROM UNTIL [OUT_DIR]   (dates as YYYY-MM-DD)

Keeps a paper only if its first category is cs.CV and its own license is CC BY 4.0 or CC BY-SA 4.0,
and writes it to OUT_DIR/cc-by-4.0/<id>.txt or OUT_DIR/cc-by-sa-4.0/<id>.txt: the title, a blank
line, the abstract. OUT_DIR defaults to ../p2-raw, outside the repo. Waits 3 s between requests.
"""

from __future__ import annotations

import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ENDPOINT = "https://oaipmh.arxiv.org/oai"
NS = {"oai": "http://www.openarchives.org/OAI/2.0/", "arxiv": "http://arxiv.org/OAI/arXiv/"}
LICENSES = {
    "http://creativecommons.org/licenses/by/4.0/": "cc-by-4.0",
    "http://creativecommons.org/licenses/by-sa/4.0/": "cc-by-sa-4.0",
}
WAIT_S = 3


def fetch(params: dict[str, str]) -> bytes:
    url = f"{ENDPOINT}?{urllib.parse.urlencode(params)}"
    for _ in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 503:
                raise
            wait = int(e.headers.get("Retry-After", "30"))
            print(f"  503, retrying in {wait} s", flush=True)
            time.sleep(wait)
    sys.exit(f"Gave up on {url}")


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def main() -> None:
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    start, until = sys.argv[1], sys.argv[2]
    out = Path(sys.argv[3] if len(sys.argv) == 4 else "../p2-raw")
    params = {"verb": "ListRecords", "metadataPrefix": "arXiv", "set": "cs", "from": start, "until": until}
    seen = kept = 0
    while True:
        root = ET.fromstring(fetch(params))
        error = root.find("oai:error", NS)
        if error is not None:
            if error.get("code") == "noRecordsMatch":
                break
            sys.exit(f"OAI-PMH error {error.get('code')}: {error.text}")
        for meta in root.iterfind(".//oai:record/oai:metadata/arxiv:arXiv", NS):
            seen += 1
            categories = clean(meta.findtext("arxiv:categories", "", NS)).split()
            license_dir = LICENSES.get(clean(meta.findtext("arxiv:license", "", NS)))
            if not categories or categories[0] != "cs.CV" or license_dir is None:
                continue
            arxiv_id = clean(meta.findtext("arxiv:id", "", NS))
            title, abstract = clean(meta.findtext("arxiv:title", "", NS)), clean(meta.findtext("arxiv:abstract", "", NS))
            if not (arxiv_id and title and abstract):
                continue
            folder = out / license_dir
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"{arxiv_id.replace('/', '_')}.txt").write_text(f"{title}\n\n{abstract}\n", encoding="utf-8", newline="\n")
            kept += 1
        token = root.find(".//oai:resumptionToken", NS)
        print(f"{seen} records seen, {kept} kept", flush=True)
        if token is None or not (token.text or "").strip():
            break
        params = {"verb": "ListRecords", "resumptionToken": token.text.strip()}
        time.sleep(WAIT_S)
    print(f"Done: {kept} papers written under {out}")


if __name__ == "__main__":
    main()
