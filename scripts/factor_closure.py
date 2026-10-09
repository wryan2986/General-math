#!/usr/bin/env python3
"""Report exact factor-language closure for a dyadic sequence prefix."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from shallit9 import factor_closure

parser = argparse.ArgumentParser()
parser.add_argument("--iterations", type=int, default=15)
args = parser.parse_args()
print(json.dumps(factor_closure(args.iterations), indent=2))

