import json
import re
import sys
from optparse import OptionParser
from pathlib import Path


def is_file(parser: OptionParser, path: Path):
    if not path.is_file():
        parser.error(f"File not found '{path}'")


if __name__ == "__main__":
    script_dir = Path(__file__).absolute().parent

    parser = OptionParser()

    parser.add_option(
        "-i",
        "--input",
        metavar="FILE",
        default=script_dir / "loot.json",
        help="Path to 'loot.json'",
    )
    parser.add_option(
        "-o",
        "--output",
        metavar="FILE",
        default=script_dir / "loot.no-token.json",
    )

    (options, args) = parser.parse_args()

    loot_path = Path(options.input)
    is_file(parser, loot_path)

    loot: list[dict]
    with open(
        loot_path,
        encoding="utf-8-sig",
    ) as f:
        loot = json.loads(f.read())

    faction_token_pat = re.compile(r"^token_")
    memory_item_pat = re.compile(r"^artmat_")

    for i, item in enumerate(loot):
        if (
            item["tokenCost"]
            and not faction_token_pat.search(item["name"])
            and not memory_item_pat.search(item["name"])
        ):
            print(f"{i}, {item["name"]}: {item["tokenCost"]} -> 0", file=sys.stderr)
            item["tokenCost"] = 0

    output_path = Path(options.output)

    with open(output_path, "wb") as f:
        f.write(json.dumps(loot, ensure_ascii=False, indent=2).encode())

    print(f"\nSaved to '{output_path}'", file=sys.stderr)
