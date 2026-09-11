# German Local Manifesto Project (GLMP)

The German Local Manifesto Project (GLMP) provides a systematically documented, versioned and reproducible corpus of municipal election programmes in Germany. The project is designed as research infrastructure: GLMP provides source documents and metadata; researchers conduct their own substantive or policy-position analyses.

## Core data principle

GLMP distinguishes **documents** from **document uses**. A document is a unique text, identified by its SHA-256 content hash. A document use records that this document was used by a party/group for a particular municipality and election. This distinction is essential when one county-level or other higher-level programme is used in several municipalities.

## Repository structure

- `manifestos/` – 2,320 TXT files in the main corpus.
- `programmes_additional/` – 166 additional programme files, kept separately because their programme level differs from the municipal programme corpus.
- `data/documents.csv` – 2,313 unique documents.
- `data/document_uses.csv` – 2,323 documented uses.
- `data/glmp_manifestos_final.csv` – consolidated researcher-facing observation table.
- `data/municipalities.csv` – municipality reference table with AGS.
- `data/additional_program_files.csv` – classification and provenance of the additional 166 files.
- `data/file_inventory.csv` – file-level provenance inventory.
- `metadata/manifestos.csv` – legacy/main-corpus parsing output.
- `metadata/source/` – source reference tables used for filename parsing and municipality mapping.
- `scripts/` – reproducible metadata/build scripts.
- `docs/` – data model, data dictionary and quality-control documentation.

## Document classification

`document_type` distinguishes:

1. `Kommunalwahlprogramm Gemeinde`
2. `Grundsatzprogramm`
3. `anderes kommunales Wahlprogramm`

`program_scope` is separate and identifies the substantive/electoral level of the document, e.g. `Gemeinde`, `Landkreis`, `Landkreis und Gemeinden`, `Land`, `Region` or `übergeordnet`.

## Reproducibility

The TXT corpus is distributed as source data. Metadata are generated from filenames, reference tables and explicit classification decisions. The parser does not infer party identity from manifesto text when a legacy filename abbreviation is unresolved; manual overrides are explicitly documented.

## AGS

AGS is attached to the municipality/document-use level. The current working AGS reference represents the 2024 municipality reference state. Historical boundary/name crosswalks are not silently inferred and should be added separately when historical administrative identifiers are required.

## Current status

This repository package is a working research-infrastructure release. Before a public release, the project should add the final licence statement, citation information, release/version number, historical AGS crosswalks where required, and a formal changelog.
