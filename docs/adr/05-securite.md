# ADR-05 — Accès ciblés et exploitation traçable

Statut : retenu dans le cas déployé, 23 octobre 2026.

**Contexte.** Les données de déplacement et les abonnés nécessitent des accès restreints et un secret de pseudonymisation protégé.

**Décision.** Identités managées, RBAC ciblé et sel existant dans Key Vault ; protéger les entrées et sorties sensibles, exclure les identifiants de Gold.

**Alternatives.** Secrets en code, clés de stockage ou droits administrateur : exposition et périmètre excessifs.

**Conséquences.** Silver pseudonymisé reste une donnée personnelle. Aucun sel ni donnée individuelle n’est publié. Une politique de rétention et un traitement des historiques seraient requis pour l’effacement ; aucune purge n’a été exécutée.
