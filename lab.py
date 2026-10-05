"""Local no-install entry point; trusted owned source only."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from constraint_lab.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
