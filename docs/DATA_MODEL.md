# GLMP Data Model

## 1. Basic principle

The GLMP separates **documents** from **document uses**.

This is necessary because the same programme can be used by one
political actor in several municipalities. This is especially relevant
for county-level programmes: a party may prepare one
Kreistagswahlprogramm and use it as its only available programme in
several municipalities.

Treating every municipal use as a separate document would artificially
duplicate the same text.

## 2. Core relationship

``` text
                 ┌────────────────────┐
                 │     documents      │
                 │                    │
                 │ document_id        │
                 │ content_hash       │
                 │ document_type      │
                 │ program_scope      │
                 │ election_year     │
                 └─────────┬──────────┘
                           │
                           │ 1 : N
                           │
                 ┌─────────▼──────────┐
                 │   document_uses    │
                 │                    │
                 │ document_use_id    │
                 │ document_id        │
                 │ municipality       │
                 │ ags                │
                 │ party              │
                 │ election_year      │
                 │ document_type      │
                 │ program_scope      │
                 └─────────┬──────────┘
                           │
                           │ municipality
                           │
                 ┌─────────▼──────────┐
                 │   municipalities   │
                 │                    │
                 │ municipality       │
                 │ ags                │
                 │ state              │
                 └────────────────────┘
```

## 3. Document level

`documents.csv` represents the **unique text document**.

A document is identified at the content level through `content_hash`. If
two source files contain byte-identical cleaned TXT content, they are
represented by the same `document_id`.

The document-level record should therefore answer questions such as:

-   What is this text?
-   What programme type is it?
-   What territorial/electoral scope does it have?
-   Which election year is associated with it?
-   How many source files contain this exact text?

## 4. Use level

`document_uses.csv` represents the **association of a document with a
municipal research observation**.

It answers questions such as:

-   Which municipality is this document associated with?
-   Which party/group used it there?
-   Which election year does the observation refer to?
-   Was it part of the main corpus or the additional collection?

The same `document_id` can therefore occur in several `document_use_id`
records.

## 5. Why municipality and programme scope are separate

This distinction is fundamental.

A document may be:

``` text
municipality = Municipality A
program_scope = Landkreis
```

This means that the document is represented for Municipality A, but the
document itself is a county-level programme.

It may simultaneously be represented for:

``` text
Municipality B
Municipality C
Municipality D
```

without becoming four different documents.

This allows researchers to distinguish between:

1.  **the geographical unit for which the document is used in the
    corpus**, and
2.  **the territorial/electoral level addressed by the document
    itself**.

## 6. Research consequences

The data model permits different analytical samples without changing the
underlying corpus.

For example:

### Municipal-programme sample

``` text
program_scope = Gemeinde
```

This can be used when the research question specifically requires
programmes written for municipal council elections.

### County-programme sample

``` text
program_scope = Landkreis
```

This can be used for research on county-level programmes.

### All programmes used in municipalities

Researchers can instead select all `document_uses` associated with a
municipality, regardless of programme scope.

The GLMP does not prescribe which of these samples is substantively
correct. It provides the information required to make the selection
explicit and reproducible.

## 7. Document type vs. programme scope

These variables should not be treated as synonyms.

`document_type` describes the **kind of document**.

`program_scope` describes the **level addressed by the document**.

This allows combinations such as:

``` text
document_type = anderes kommunales Wahlprogramm
program_scope = Landkreis
```

or

``` text
document_type = anderes kommunales Wahlprogramm
program_scope = Landkreis und Gemeinden
```

## 8. Content identity and reuse

Identical text is not automatically a quality problem.

A party may deliberately reuse a programme across several
municipalities. The correct representation is:

``` text
one content_hash
        ↓
one document_id
        ↓
multiple document_use_id records
```

This preserves both textual identity and geographical use.

## 9. AGS

The AGS belongs conceptually to the **municipality/use level**, not to
the document itself. A document can be used in multiple municipalities
and therefore can be associated with multiple AGS values through
`document_uses`.

The current working AGS reference reflects the 2024 municipality state.
Historical administrative changes require an explicit historical
crosswalk in future releases.

## 10. Researcher-facing consolidated table

`glmp_manifestos_final.csv` provides a convenient one-row-per-use
representation for researchers who do not need to work with the
normalized relational structure directly.

The normalized tables remain the authoritative representation of the
document/use relationship.
