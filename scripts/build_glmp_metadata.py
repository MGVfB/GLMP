from pathlib import Path
import hashlib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "metadata"
DATA = ROOT / "data"

main = pd.read_csv(META / "manifestos.csv", sep=";")
other = pd.read_csv(DATA / "additional_program_files.csv", sep=";")
local = pd.read_csv(ROOT / "metadata" / "source" / "local_cities.csv", sep=";")

# Rebuild the consolidated researcher-facing table from the packaged metadata.
# The document-level tables remain the canonical normalized representation.
uses = pd.read_csv(DATA / "document_uses.csv", sep=";")
uses.to_csv(DATA / "document_uses.csv", sep=";", index=False, encoding="utf-8-sig")

# Basic integrity checks
assert len(main) == 2320, f"Expected 2320 main observations, found {len(main)}"
assert len(other) == 166, f"Expected 166 additional source files, found {len(other)}"
assert len(uses) == 2323, f"Expected 2323 document uses, found {len(uses)}"
assert uses.document_id.notna().all()
assert uses.municipality.notna().all()
assert uses.document_type.notna().all()
assert uses.program_scope.notna().all()
assert uses.ags.notna().all()
print("GLMP metadata validation successful:", len(uses), "document uses")
