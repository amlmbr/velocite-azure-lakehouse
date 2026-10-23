# ADR-03 — État Silver par clé et version

Statut : retenu dans le cas déployé, 23 octobre 2026.

**Contexte.** Des doublons et des versions anciennes peuvent réapparaître lors du rejeu.

**Décision.** Dédupliquer par location_id, sélectionner la dernière version et appliquer seulement les versions strictement plus récentes dans Delta ; isoler les rejets.

**Alternatives.** Append simple : doublons ; DELETE/INSERT : cohérence et rejeu plus difficiles à maîtriser.

**Conséquences.** Le jeu isolé de huit entrées produit quatre lignes et trois rejets. Le rejeu ne crée pas de commit Delta supplémentaire. Les conflits de contenu à version identique restent à traiter.
