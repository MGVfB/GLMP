# GLMP Data Dictionary

This document describes the main machine-readable data files in the
repository.

## 1. `data/documents.csv`

**Unit of observation:** one unique document/content.

A document is represented once even when the same text occurs in several
source files or is used in several municipalities.

  ------------------------------------------------------------------------
  Variable                            Definition
  ----------------------------------- ------------------------------------
  `document_id`                       Stable GLMP identifier for the
                                      unique document record.

  `filename`                          Representative/source filename
                                      associated with the document.

  `document_type`                     Document classification:
                                      `Kommunalwahlprogramm Gemeinde`,
                                      `Grundsatzprogramm`, or
                                      `anderes kommunales Wahlprogramm`.

  `program_scope`                     Political/electoral level addressed
                                      by the document, e.g. `Gemeinde`,
                                      `Landkreis`,
                                      `Landkreis und Gemeinden`, `Land`,
                                      `Region`, or `übergeordnet`.

  `election_year`                     Election year associated with the
                                      document where applicable. Blank for
                                      documents without a coded election
                                      year, such as undated/basic
                                      programmes.

  `content_hash`                      SHA-256 hash of the cleaned TXT
                                      content. This is the principal
                                      content-level identifier used to
                                      detect identical documents.

  `bytes`                             Size of the represented TXT file in
                                      bytes.

  `source_count`                      Number of source-file occurrences
                                      represented by this document.

  `main_file_count`                   Number of occurrences in the main
                                      corpus.

  `other_file_count`                  Number of occurrences in the
                                      additional programme collection.
  ------------------------------------------------------------------------

### Interpretation

`document_id` identifies a document record. `content_hash` identifies
the document at the level of its exact TXT content. Multiple source
files can therefore point to the same document.

------------------------------------------------------------------------

## 2. `data/document_uses.csv`

**Unit of observation:** one documented use/association of a document
with a municipality and election.

  -----------------------------------------------------------------------
  Variable                            Definition
  ----------------------------------- -----------------------------------
  `document_use_id`                   Stable identifier for the
                                      document-use record.

  `document_id`                       Foreign-key-style link to
                                      `documents.csv`.

  `manifesto_id`                      Existing GLMP identifier for a
                                      main-corpus observation where
                                      applicable.

  `municipality`                      Municipality for which the document
                                      is represented/used in GLMP.

  `state`                             Federal state of the municipality.

  `ags`                               8-digit Amtlicher Gemeindeschlüssel
                                      for the municipality in the current
                                      working reference.

  `party`                             Party, electoral group or political
                                      actor associated with the use.

  `party_abbreviation`                Standardized abbreviation where one
                                      is available.

  `election_year`                     Election year of the municipal
                                      observation.

  `document_type`                     Classification of the document used
                                      in this observation.

  `program_scope`                     Political/electoral level addressed
                                      by the document.

  `use_type`                          Provenance/use category, currently
                                      including `main_corpus_observation`
                                      and `additional_program_use`.

  `source_filename`                   Filename from the source collection
                                      associated with this use.

  `source`                            Source collection: `main` or
                                      `other`.

  `ags_source`                        Method/reference used for the
                                      current AGS assignment.

  `content_hash`                      SHA-256 hash of the document
                                      content.
  -----------------------------------------------------------------------

### Interpretation

The municipality in this table answers **where the document was
used/represented in the GLMP**.

`program_scope` answers **which political/electoral level the document
itself addresses**.

These concepts must not be conflated.

------------------------------------------------------------------------

## 3. `data/glmp_manifestos_final.csv`

**Unit of observation:** one document use.

This is the consolidated researcher-facing table. It contains the
principal variables needed to construct municipality-level research
samples without requiring users to join the two core relational tables.

The `filename` variable corresponds to the source filename for the
particular use.

------------------------------------------------------------------------

## 4. `data/municipalities.csv`

**Unit of observation:** one municipality.

  -----------------------------------------------------------------------
  Variable                            Definition
  ----------------------------------- -----------------------------------
  `ags`                               8-digit Amtlicher Gemeindeschlüssel
                                      in the current working municipality
                                      reference.

  `municipality`                      Municipality name.

  `state`                             Federal state.

  `ags_source`                        Source/method used for the current
                                      AGS assignment.
  -----------------------------------------------------------------------

The current reference reflects the 2024 municipality state. It is not a
historical AGS reconstruction.

------------------------------------------------------------------------

## 5. `data/additional_program_files.csv`

**Unit of observation:** one file from the additional programme
collection.

  -----------------------------------------------------------------------
  Variable                            Definition
  ----------------------------------- -----------------------------------
  `filename`                          Filename in the additional
                                      programme collection.

  `content_hash`                      SHA-256 hash of the file content.

  `bytes`                             File size in bytes.

  `document_type`                     GLMP document classification.

  `program_scope`                     Political/electoral level addressed
                                      by the document.

  `classification_reason`             Reason recorded for the
                                      classification.

  `municipality_used`                 Municipality for which the document
                                      is represented/used in GLMP.

  `party`                             Party/group associated with the
                                      use.

  `election_year`                     Election year.

  `matched_main_by_content`           Whether the file's content is also
                                      present in the main corpus.

  `matched_main_filenames`            Main-corpus filename(s) with
                                      identical content where applicable.

  `document_id`                       Link to the unique document record.

  `main_use_id`                       Corresponding main-corpus use
                                      identifier where applicable.

  `ags`                               Municipality AGS.

  `ags_source`                        AGS assignment source/method.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 6. `data/file_inventory.csv`

**Unit of observation:** one source file.

This table provides file-level provenance across both the main and
additional collections.

Important variables include:

-   `source` --- `main` or `other`
-   `filename`
-   `content_hash`
-   `bytes`
-   `manifesto_id`
-   `municipality`
-   `state`
-   `party`
-   `party_abbreviation`
-   `election_year`
-   `document_type`
-   `program_scope`
-   `classification_reason`
-   `path`

------------------------------------------------------------------------

## Classification categories

### `document_type`

**`Kommunalwahlprogramm Gemeinde`**\
A programme prepared for the municipal level of a specific municipality,
such as a city council or municipal council election.

**`Grundsatzprogramm`**\
A basic/general party programme used in the corpus without being
classified as a municipality-specific election programme.

**`anderes kommunales Wahlprogramm`**\
A municipal-election-related programme whose scope is not a specific
municipality, for example a county council programme or another
programme addressing several municipalities or a higher territorial
level.

### `program_scope`

The scope is coded independently of document type. Current values are:

-   `Gemeinde`
-   `Landkreis`
-   `Landkreis und Gemeinden`
-   `Land`
-   `Region`
-   `übergeordnet`

The combination is intentional. For example, a document may have
`document_type = anderes kommunales Wahlprogramm` and
`program_scope = Landkreis`, while being used for several
municipalities.

## Identifiers

The principal relationships are:

``` text
documents.document_id
        │
        └──────────< document_uses.document_id

document_uses.municipality
        │
        └──────────> municipalities.municipality
                         │
                         └── ags
```

`content_hash` is used to identify identical text content across files.

## Research recommendation

Researchers should not assume that every document associated with a
municipality is a municipality-specific election programme. The
appropriate sample should be defined explicitly using `document_type`
and/or `program_scope`.
