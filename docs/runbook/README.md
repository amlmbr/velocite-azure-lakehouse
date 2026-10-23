# Runbook VéloCité — exploitation et reprise

**Entrée :** `PL_00_ORCHESTRATE_CERTIFIED_V2`, factory `adf-vct26a7b9`, groupe `rg-velocite-dev`.

1. **Avant lancement.** Vérifier les exécutions actives/Queued, le crédit et le budget. Garder `TR_DAILY_PARIS_V2` arrêté tant que le coût récurrent n'est pas accepté. Ne pas ouvrir de session Debug persistante. En production, conserver `validation_mode=false`.
2. **Lancement unique.** Déclencher le maître une fois. Le Run ID identifie les lots Raw et le snapshot. Le paramètre de date météo vide désigne J-1 en heure de Paris. Ne pas relancer un traitement identique encore actif.
3. **Suivi.** Contrôler CaptureBounds → IngestSQL → Silver si fichier présent → météo → REST → Analytics → QualityGate → snapshot → pointeur → commits → relecture des watermarks. Les noms exacts et expressions sont dans les exports JSON.
4. **Validation.** Lire les métriques qualité et `consumption/current.json`. Vérifier le lot, la date météo, le mode, `sla_met` et les bornes. Charger exclusivement le snapshot désigné ; combiner tous les snapshots doublerait les résultats.
5. **Échec avant publication.** Conserver le pointeur précédent. Examiner le message de l'activité, le schéma réel, les chemins et la quarantaine du lot. Corriger la cause puis relancer une fois. Ne jamais avancer le watermark manuellement pour masquer un échec.
6. **Échec après publication.** Un snapshot peut être certifié avant un échec de commit SQL. Comparer pointeur et bornes SQL, puis reprendre idempotemment. L'ancien lot ne doit pas écraser une version Silver plus récente.
7. **Rejeu d’une période.** Conserver les lots Raw et le pointeur courant. Le lookback automatique couvre sept jours de modification ; `target_date` ne choisit que la journée météo. Pour une période SQL plus ancienne, préparer et contrôler une extraction bornée dans un chemin isolé, tester Silver et les agrégats, puis valider le candidat avant toute publication. Ne pas abaisser les watermarks de production.
8. **Quarantaine.** Lire les motifs du lot, corriger la cause à la source avec une nouvelle version `modifie_le`, rejouer, puis conserver les traces de résolution ; ne pas réinjecter une ligne sans contrôle.
9. **Sans données nouvelles.** Vérifier les attentes Raw à zéro, l'absence d'exécution Silver et la conservation des totaux. Météo et REST peuvent encore se rafraîchir. Ne pas présenter une configuration d'absence de fichier comme un test réussi sans Run ID.
10. **Après traitement.** Conserver statut, horaires et métriques ; vérifier l'alerte Monitor et les coûts différés. Aucun email ou groupe d'action n'est configuré sans destinataire validé. Arrêter les essais terminés ; laisser le déclencheur quotidien arrêté.

**Interdictions :** aucun sel affiché/régénéré, aucun droit administrateur ajouté pour contourner un défaut, aucune purge Raw/Delta ou suppression source sans sauvegarde et accord adapté.
