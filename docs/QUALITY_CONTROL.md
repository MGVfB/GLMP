# GLMP Quality Control

Current packaged release checks:

- Main corpus: 2,320 TXT files.
- Additional programme collection: 166 TXT files.
- Unique documents: 2,313.
- Document uses: 2,323.
- Municipalities: 248.
- All packaged document uses have a municipality, document type, programme scope and AGS.
- Document identity uses SHA-256 content hashes.
- Duplicate content is retained as one document with multiple source/use records where appropriate.
- The additional collection is retained separately to preserve provenance.

## Interpretation of identical texts

Identical content is not automatically an error. A party may deliberately reuse the same programme in several municipalities. Such cases are represented by one `document_id` and multiple `document_use_id` records.

## AGS reference state

The AGS field uses the **31 December 2024 municipality reference state** for all observations, including historical election years. This is intentional: the current GLMP release does not reconstruct historical municipal boundaries or historical AGS values. The stable 2024 reference is used consistently across the corpus. A historical crosswalk can be added in a future release if newly added municipalities make territorial changes relevant.
