# German Local Manifesto Project (GLMP)

The **German Local Manifesto Project (GLMP)** is a research
infrastructure for the systematic collection, documentation, versioning
and reproducible use of local election programmes in Germany.

GLMP provides **source documents and structured metadata**. It does not
impose a substantive policy coding scheme or a preferred method for
measuring political positions. Researchers can use the corpus to conduct
their own analyses, including the calculation of local policy positions.

## What the repository contains

The repository contains two related programme collections:

-   `manifestos/` --- the main corpus of 2,320 TXT files.
-   `programmes_additional/` --- 166 additional TXT files containing
    programmes that differ in their electoral or political scope from
    the main municipal-programme corpus.

The additional collection is retained separately so that the provenance
and scope of these documents remain transparent.

In the current working dataset:

-   **2,313 unique documents** are identified by SHA-256 content hash.
-   **2,323 document uses** are recorded.
-   **248 municipalities** are represented.
-   All 2,320 files of the main corpus and all 166 files of the
    additional collection are represented in the file inventory.

Of the 166 additional files, 163 contain text that is also present in
the main corpus, while 3 represent new document contents. Identical text
is not automatically treated as an error: a party may reuse the same
programme in several municipalities.

## The central data principle: documents vs. document uses

GLMP distinguishes between the **document itself** and its **use for a
municipality**.

A document is stored once in `data/documents.csv`. A record in
`data/document_uses.csv` records that this document is associated with a
particular party, municipality and election.

This distinction is essential because a party may use the same
county-level election programme in several municipalities without
preparing a separate municipal programme for each municipality.

Conceptually:

``` text
one document
      │
      ├── use in municipality A
      ├── use in municipality B
      └── use in municipality C
```

This avoids artificial duplication while preserving the information
needed for municipality-level research.

## Document classification

GLMP distinguishes three document types:

1.  `Kommunalwahlprogramm Gemeinde`
2.  `Grundsatzprogramm`
3.  `anderes kommunales Wahlprogramm`

The variable `program_scope` is separate from `document_type`. It
records the political/electoral level addressed by the document, for
example:

-   `Gemeinde`
-   `Landkreis`
-   `Landkreis und Gemeinden`
-   `Land`
-   `Region`
-   `übergeordnet`

This distinction matters for research. A document can be **used for a
municipality** while actually being a **county-level programme**.
Researchers who want to calculate positions specifically from municipal
council programmes can therefore filter accordingly.

The GLMP does not decide which type of programme researchers should use
for a particular research question. It documents the distinction so that
researchers can make that decision transparently.

## Main data files

### `data/documents.csv`

One row per unique document/content. The document is identified by its
SHA-256 content hash.

### `data/document_uses.csv`

One row per documented use of a document for a municipality/election
observation. This is the principal relational table for linking
documents to municipalities.

### `data/glmp_manifestos_final.csv`

A consolidated researcher-facing table with one row per document use.

### `data/municipalities.csv`

Municipality reference table containing municipality names, federal
states and AGS.

### `data/additional_program_files.csv`

File-level documentation of the 166 additional programme files,
including their classification, provenance and links to the
corresponding document/use records.

### `data/file_inventory.csv`

File-level inventory of both programme collections.

## Programme files

The programme files are provided as cleaned TXT files. GLMP does not
display full manifesto texts as substantive web content; the repository
provides the machine-readable source files for download and analysis.

Filenames should be treated as source/provenance information, not as the
sole identifier of a document. Document identity is represented by
`document_id` and, at the content level, by `content_hash`.

## AGS

The `ags` variable is attached to the municipality/document-use level.

The current working reference uses the **2024 municipality reference
state**. It is not intended to be a complete reconstruction of
historical AGS values. Municipal boundaries and names can change over
time. Historical administrative identifiers should therefore be added
through an explicit historical crosswalk rather than inferred silently.

## Reproducibility

The metadata are generated and maintained through documented processing
steps. The repository contains the scripts and source reference tables
used for the current metadata construction.

The party mapping for legacy filenames uses the supplied
party-abbreviation reference as the primary source. Where abbreviations
are ambiguous or cannot be resolved mechanically, explicit manual
decisions are retained rather than guessing from manifesto text.

## Repository structure

``` text
GLMP/
├── data/
├── docs/
├── manifestos/
├── metadata/
├── programmes_additional/
├── scripts/
├── CITATION.cff
└── README.md
```

See:

-   `docs/DATA_MODEL.md` for the relational structure.
-   `docs/DATA_DICTIONARY.md` for variable definitions.
-   `docs/QUALITY_CONTROL.md` for quality-control procedures and current
    results.

## Research use

GLMP is intended as an infrastructure for reproducible research on local
political communication and election programmes. Researchers remain
responsible for defining their analytical sample and coding strategy.

In particular, researchers should explicitly state whether their
analysis uses:

-   only `program_scope = Gemeinde`,
-   county-level or other programmes,
-   all programmes used in a municipality,
-   or another clearly defined selection rule.

## Current status

This repository represents a working research-infrastructure version.
Future releases should add a formal version/changelog system, a final
licence statement, and historical AGS crosswalks where required.
