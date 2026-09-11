# GLMP Data Model

## Why documents and uses are separate

A party may use one and the same county-level election programme in several municipalities. Storing the programme once and linking it to several municipalities prevents artificial duplication while preserving the information needed for municipal research.

### Relationship

`documents` 1 — N `document_uses`

A unique document is identified by its SHA-256 `content_hash`. A `document_use` connects that document to a municipality, party and election year.

## Research implications

Researchers can filter by `program_scope` to distinguish, for example, municipal council programmes from county council programmes. They can also filter by municipality to reconstruct which programme a party used in a given municipality.

The GLMP does not prescribe substantive policy coding or a preferred policy-position measure.
