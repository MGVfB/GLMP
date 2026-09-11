# GLMP Data Dictionary

## `data/documents.csv`

One row per unique document/content.

| Variable | Meaning |
|---|---|
| `document_id` | Stable GLMP identifier for the unique document/content. |
| `filename` | Source TXT filename used in the GLMP corpus. |
| `document_type` | Type of programme: municipal programme, basic programme, or another municipal programme. |
| `program_scope` | Political/electoral level addressed by the document. |
| `election_year` | Election year when applicable; blank for undated/basic programmes. |
| `content_hash` | SHA-256 hash of the TXT content; primary content-level deduplication key. |
| `bytes` | File size in bytes. |
| `source_count` | Number of source-file occurrences represented by this document. |
| `main_file_count` | Number of occurrences in the main corpus. |
| `other_file_count` | Number of occurrences in the additional-programme collection. |

## `data/document_uses.csv`

One row per documented use of a document for a municipality/election observation.

| Variable | Meaning |
|---|---|
| `document_use_id` | Stable identifier for the use/observation. |
| `document_id` | Link to `documents.csv`. |
| `manifesto_id` | Existing GLMP manifesto/observation identifier where applicable. |
| `municipality` | Municipality for which the document is represented/used in GLMP. |
| `state` | German federal state. |
| `ags` | 8-digit Amtlicher Gemeindeschlüssel at the municipality level, using the 31 December 2024 municipality reference state. The same reference AGS is used for observations from earlier election years. |
| `party` | Party/group associated with the use. |
| `party_abbreviation` | Standardized abbreviation where available. |
| `election_year` | Election year. |
| `document_type` | Programme classification. |
| `program_scope` | Level addressed by the programme. |
| `use_type` | Provenance/use category, e.g. main corpus observation or additional programme use. |
| `source_filename` | Source filename associated with the use. |
| `source` | Source collection (`main` or `other`). |
| `ags_source` | Source/method used for the 2024 AGS assignment. |
| `content_hash` | SHA-256 content hash. |

## `data/glmp_manifestos_final.csv`

Consolidated researcher-facing table: one row per document use. `filename` is the source filename for that use.

## Classification principle

The municipality in `document_uses.csv` records **where the document was used in the corpus**; `program_scope` records **the level for which the document itself was written/addressed**. These must not be conflated.

## AGS reference principle

The GLMP currently uses a single municipality reference state: **31 December 2024**. The AGS is therefore a stable current municipality identifier and is not reconstructed historically for older election years. If future releases add municipalities affected by relevant territorial changes, a separate historical crosswalk can be introduced without changing the current identifier principle.
