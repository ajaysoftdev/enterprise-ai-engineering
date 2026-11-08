# Reference sources — Enterprise MDM and Data Governance

## Governance, semantics and quality
- [EDM Council](https://edmcouncil.org/) — industry data-management and data-governance frameworks, including DCAM.
- [W3C RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/) — graph-based representation of entities and relationships.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/) — provenance and lineage model.
- [OpenMetadata](https://docs.open-metadata.org/) — metadata catalogue, ownership, glossary, quality and lineage concepts.
- [Great Expectations](https://docs.greatexpectations.io/) — declarative data-quality validation patterns.

## Matching and integration
- [Record Linkage Toolkit](https://recordlinkage.readthedocs.io/) — reproducible probabilistic record-linkage techniques.
- [OpenAPI](https://spec.openapis.org/oas/latest.html) — versioned service contracts.
- [CloudEvents](https://cloudevents.io/) — event envelope for master-data changes.

## Apply these references to this project
Define canonical entities and identifiers before matching. Make match thresholds, survivorship precedence and steward overrides configurable and explainable. Keep source values and lineage; never silently overwrite conflicting records or treat fuzzy-match scores as definitive identity proof.
