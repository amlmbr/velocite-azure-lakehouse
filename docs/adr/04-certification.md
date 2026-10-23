# ADR-04 — Certification avant publication

Statut : retenu dans le cas déployé, 23 octobre 2026.

**Contexte.** Un produit partiellement écrit ne doit pas devenir visible aux consommateurs.

**Décision.** Construire les candidats, mesurer les six dimensions qualité et publier un snapshot certifié, puis current.json et les commits SQL.

**Alternatives.** Publication directe dans un chemin partagé, exposant des résultats incomplets ; transaction distribuée non disponible dans cette chaîne.

**Conséquences.** Les lecteurs suivent un seul snapshot. Une reprise idempotente est nécessaire entre pointeur et commits. Le succès en validation ne prouve pas le SLA ; validation_mode reste faux par défaut.
