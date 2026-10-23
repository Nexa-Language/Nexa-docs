"""Refresh only explicitly reviewed capability or example fingerprints."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from scripts.check_docs import digest, read_examples


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--capability", action="append", default=[])
    parser.add_argument("--page", action="append", default=[])
    parser.add_argument("--note", required=True, help="What changed and which claims/scenarios were reviewed")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    inventory_path = root / "docs/inventory.json"
    inventory = json.loads(inventory_path.read_text())
    if not args.capability and not args.page:
        parser.error("select at least one reviewed capability or page")
    unknown = set(args.capability) - {item["id"] for item in inventory["capabilities"]}
    unknown |= set(args.page) - {item["path"] for item in inventory["pages"]}
    if unknown:
        parser.error(f"unregistered selections: {', '.join(sorted(unknown))}; register new records manually")
    review = {"at": datetime.now(UTC).isoformat(), "note": args.note}
    runtime = args.runtime.resolve()
    for capability in inventory["capabilities"]:
        if capability["id"] not in args.capability:
            continue
        for source in capability["provenance"]:
            path = (runtime / source["path"]).resolve()
            if not path.is_relative_to(runtime):
                parser.error(f"source outside runtime: {source['path']}")
            content = path.read_text()
            if source.get("symbol") and source["symbol"] not in content:
                parser.error(f"missing reviewed symbol: {source['path']}: {source['symbol']}")
            source["sha256"] = digest(content)
        capability["review"] = review
    actual = read_examples(root)
    for example in inventory["examples"]:
        if example["page"] in args.page:
            example["sha256"] = digest(actual[(example["page"], example["block"])].source)
            example["review"] = review
    head, tree = subprocess.check_output(["git", "-C", str(runtime), "rev-parse", "HEAD", "HEAD^{tree}"], text=True).splitlines()
    inventory["runtime"].update(
        version=(runtime / "VERSION").read_text().strip(),
        git_head=head,
        source_tree=tree,
        verification_checkout_head=head,
        dirty=bool(subprocess.check_output(["git", "-C", str(runtime), "status", "--porcelain"], text=True).strip()),
    )
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n")
    print(f"Reviewed {len(args.capability)} capabilities and {len(args.page)} pages; run verification before committing")


if __name__ == "__main__":
    main()
