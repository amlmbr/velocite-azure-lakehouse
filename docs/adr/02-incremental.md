# ADR-02 — Incrémental borné

Statut : retenu dans le cas déployé, 23 octobre 2026.

**Contexte.** Les locations peuvent être corrigées après leur date métier et la copie quotidienne complète est évitable.

**Décision.** Capturer les bornes supérieures de modifie_le, lire avec sept jours de reprise et avancer les watermarks après certification.

**Alternatives.** Recharge complète plus coûteuse ; CDC plus complet pour les suppressions, mais non déployé.

**Conséquences.** Toute correction doit augmenter modifie_le. La fenêtre porte sur la modification. Les suppressions physiques ne sont pas propagées ; les contrôles doivent bloquer les divergences concurrentes.
