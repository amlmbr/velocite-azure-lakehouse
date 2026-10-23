# Résultats des dix scénarios

| Scénario | Vérification réelle | Résultat et périmètre |
|---|---|---|
| 1. Ingestion initiale | CopyLocations 200 000 lues/copiées en 18 s ; abonnés 5 000 en 14 s ; stations 50 en 14 s. CSV météo : 4 lignes. REST : 1 enveloppe JSON lue/copée contenant 1 519 stations. | Réussi. Les métriques de copie et les comptages sémantiques sont distincts. |
| 2. Incrémental | Ancienne version ignorée, dernière version retenue et insertion sur fixture ; run final avec attentes Raw zéro, copies SQL incrémentales évitées et Silver non lancé. | Réussi dans ces périmètres. Modification directe de dbo.locations non exécutée : identité ADF sans UPDATE. |
| 3. Correction J-7 | Événement historique de la fixture modifié avec version plus récente ; vérification Delta puis agrégats Gold en heure de Paris. | Réussi sur jeu isolé. Gold : 4 locations, 2 jours, 3 clés jour/station, montant 16,00. |
| 4. Idempotence | Deux exécutions réussies du même input INT96 ; Delta isolé reste en version 1 avec 4 clés uniques. Le run de production sans changement conserve 200 000 locations et le total 999 995,00. | Réussi. Les totaux API peuvent changer entre deux collectes, ce qui est normal. |
| 5. Qualité / quarantaine | Trois invalides : montant négatif, fin avant début, début absent. Rejeu avec batch_id et rejection_reason explicites. Gate positif et gate négatif. | 3 rejets annotés ; le gate négatif échoue comme attendu et ne publie pas sa branche Gold. |
| 6. Sécurité | Accès Key Vault et stockage par identités existantes ; recalcul en mémoire des 200 000 pseudonymes ; can_commit=1, can_update_locations=0, db_owner=0. | Réussi. Aucun sel exporté/régénéré ni droit élargi. Authentification SQL exclusivement Entra non attestée. |
| 7. Orchestration | c137cb82-4a6e-4412-adbf-a3ea52b751ea, du 23/10/2026 10:19:38 au 10:26:39 Paris. Tous les stades nécessaires, publication, commits et vérification finale. | Succeeded, 7 min 1 s. Test fonctionnel en validation_mode=true. |
| 8. Échec et reprise | Gate négatif réel ; publications bloquées si qualité invalide. Arrondi de watermark détecté après certification ; reprise gardée par le marqueur et sans Spark. | Réussi pour ces défauts observés. Le pointeur et les deux commits ne constituent pas une transaction distribuée. |
| 9. Schéma | JSON API contenant des champs supplémentaires accepté par projection. Fixture de timestamp Arrow NTZ réellement rejetée par toTimestamp, puis écriture INT96 compatible réussie. | Partiel et ciblé. Pas de test exhaustif de tous changements CSV/SQL, pas de migration arbitraire automatique. |
| 10. Fraîcheur / SLA | Météo 22/10 ; âge du flux API au début du gate : 295,97 s, seuil 900 s. Marqueur publié le 23/10 à 10:26:03 Paris, sla_met=false. | Fraîcheur configurée respectée sur ce run ; SLA quotidien avant 06:30 non démontré. |

## Principales références d'exécution

| Essai | Run ID |
|---|---|
| Analytics isolé | a0cc5b30-3dd7-41d7-8f99-449ba8e5632d |
| SQL → Silver, reprise complète | 62017e71-a4b5-4d50-80e3-b77daa66d333 |
| Fixture première passe | 4e909b9f-3a12-44de-8a89-2b1362e35f8e |
| Fixture rejeu | b2fefb75-974d-417f-a520-9fb2a489fa5e |
| Gold J-7 isolé | d2fdcf45-b441-4c9e-9ba1-b74ada3cd768 |
| Quarantaine avec motifs | f12450f9-63c3-44b9-b340-3cd48b7b734d |
| Gate négatif attendu | cb98ed44-4410-410e-b604-0ab14869d223 |
| Reprise de précision du commit | 3a47d953-a38c-403c-ac7d-a5939f687284 |
| Maître final sans modifications | c137cb82-4a6e-4412-adbf-a3ea52b751ea |

Les échecs intermédiaires sont conservés. Le premier maître de cette reprise a publié un snapshot de qualité certifiée, puis échoué à la vérification des commits. La reprise distincte et le dernier maître réussi ne changent pas rétroactivement son statut.
