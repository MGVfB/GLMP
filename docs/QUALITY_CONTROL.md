# GLMP Quality Control

## Scope of the current working release

The current working repository contains:

-   **2,320** TXT files in the main corpus.
-   **166** TXT files in the additional programme collection.
-   **2,486** source-file records in the combined file inventory.
-   **2,313** unique document/content records.
-   **2,323** document-use records.
-   **248** municipalities.
-   **14** federal states represented in the main metadata.

The additional collection contains 166 files representing **160 unique
text contents**. Of these, 163 files have content that also occurs in
the main corpus; 3 files add new document contents.

## 1. File-level checks

The main corpus was checked for:

-   duplicate filenames;
-   empty files;
-   unusually small files;
-   successful metadata mapping;
-   consistent municipality/state assignment;
-   consistent election-year parsing.

The additional collection was checked for:

-   file inventory completeness;
-   content hashes;
-   links to existing main-corpus content;
-   document classification;
-   municipality use;
-   election year;
-   programme scope.

## 2. Document identity

Document identity is established through a SHA-256 hash of the cleaned
TXT content.

This makes it possible to distinguish:

-   different files containing the same text;
-   genuinely different texts;
-   repeated use of the same text across municipalities.

The existence of identical text in several files is **not automatically
an error**.

For example, a party may reuse exactly the same county-level programme
in several municipalities. In such cases the repository should represent
one document and multiple uses.

## 3. Document/use consistency

The current data model checks that each document use links to a valid
document record and that the municipality is represented in the
municipality reference table.

The main researcher-facing observation table contains one row per
document use.

## 4. Programme classification

Each document use has a coded:

-   `document_type`;
-   `program_scope`.

No current document use is left without a classification.

The distinction is deliberately maintained because a programme can be
associated with a municipality while addressing a different territorial
level.

## 5. Party mapping

Legacy filename abbreviations were mapped using the supplied party
reference as the primary source.

Where an abbreviation is ambiguous or not sufficient to determine the
party reliably, explicit manual mappings were used. The parser does not
use the substantive text of a manifesto to guess an unresolved party
identity.

Modern filenames generally provide the party/group label directly.

## 6. Municipality mapping

Municipality names were matched against the supplied municipality
reference. ASCII/transliteration variants such as names without umlauts
were normalized where necessary.

The current working data contain 248 municipalities.

## 7. AGS

All current municipality records used in the packaged data have an AGS.

**Important limitation:** the current AGS reference represents the 2024
municipality state. It is not a historical reconstruction of the AGS for
every election year in the corpus.

For historical research, municipal boundary changes and historical
administrative identifiers should therefore be addressed through an
explicit historical crosswalk.

## 8. Exact duplicate content

Exact duplicate content is retained rather than automatically removed
from the source collections.

At the document level, identical content is collapsed into a single
`document_id`.

At the use level, each legitimate municipal use remains separately
represented.

This is intentional and preserves both:

-   textual identity; and
-   geographical/provenance information.

## 9. Interpretation of quality-control results

A clean mapping result does not imply that every substantive
classification is universally unambiguous. The purpose of the metadata
is to make the classification and provenance decisions explicit and
reproducible.

Researchers should inspect the relevant source TXT file and metadata
when their analytical sample depends on a distinction such as:

-   municipal vs. county programme;
-   own programme vs. reused programme;
-   current vs. historical municipality boundaries.

## 10. Future quality-control work

Before a formal public release, the following should be added or
expanded:

1.  historical AGS crosswalks for elections affected by territorial
    reforms;
2.  a formal release/version number;
3.  a machine-readable changelog;
4.  automated regression tests for the metadata-building scripts;
5.  a final repository licence;
6.  automated CI checks on every update.
