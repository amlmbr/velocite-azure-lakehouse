# ADR-01 — Chaîne batch Azure

Statut : retenu dans le cas déployé, 23 octobre 2026.

**Contexte.** Le besoin est une publication quotidienne avec trois sources hétérogènes et des ressources Azure déjà disponibles.

**Décision.** Réutiliser Azure SQL, ADLS Gen2, ADF et ses Mapping Data Flows ; séparer Raw, Silver Delta et snapshots Gold.

**Alternatives.** Streaming, Databricks ou plateforme supplémentaire : complexité et administration disproportionnées au cas étudié.

**Conséquences.** Spark démarre à la demande et ajoute une latence et un coût minimal. Le lineage reste documentaire, sans Purview actif.
