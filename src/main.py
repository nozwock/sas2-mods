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
        default=script_dir / "monsters.json",
        help="Path to 'monsters.json'",
    )
    parser.add_option(
        "-o",
        "--output",
        metavar="FILE",
        default=script_dir / "monsters.mage-loot.json",
    )

    (options, args) = parser.parse_args()

    monsters_path = Path(options.input)
    is_file(parser, monsters_path)

    monsters: list[dict]
    with open(
        monsters_path,
        encoding="utf-8-sig",
    ) as f:
        monsters = json.loads(f.read())

    mage_pat = re.compile(r"mancer$", flags=re.IGNORECASE)
    mage_material_pat = re.compile(r"mat_\d+$")
    gear_up_pat = re.compile(r"gear_up\d+$")

    for i, monster in enumerate(monsters):
        if mage_pat.search(monster["name"]) and mage_pat.search(monster["title"][0]):
            print(f"{i}, {monster["name"]}", file=sys.stderr)
            for i in range(len(monster["monsterField"])):
                obj = monster["monsterField"][i]

                if obj["strData"] and mage_material_pat.search(obj["strData"]):
                    chance = monster["monsterField"][i + 1]  # fData
                    max_quantity = monster["monsterField"][i + 2]  # iData

                    print(
                        f"\t{i}, {obj["strData"]}: {chance["fData"]} -> 1000",
                        file=sys.stderr,
                    )

                    chance["fData"] = 1000

                elif obj["strData"] and gear_up_pat.search(obj["strData"]):
                    chance = monster["monsterField"][i + 1]  # fData
                    max_quantity = monster["monsterField"][i + 2]  # iData

                    print(
                        f"\t{i}, {obj["strData"]}: {chance["fData"]} -> 1000",
                        file=sys.stderr,
                    )

                    chance["fData"] = 1000

    output_path = Path(options.output)

    with open(output_path, "wb") as f:
        f.write(json.dumps(monsters, ensure_ascii=False, indent=2).encode())

    print(f"\nSaved to '{output_path}'", file=sys.stderr)
