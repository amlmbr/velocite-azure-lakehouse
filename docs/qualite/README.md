# Mesures qualité et décisions

| Dimension | Règle et population | Mesure observée | Seuil bloquant |
|---|---|---|---|
| Complétude | Clés/dates requises sur 200 000 locations Silver | missing_keys=0 ; dates invalides=0 | Aucun manquant |
| Validité | Montants non négatifs, fin ≥ début, pseudonyme au format attendu ; météo numérique ; stocks API non négatifs | invalid_amounts=0 ; invalid_dates=0 ; invalid_pseudo=0 ; météo/API invalid=0 | Zéro invalide dans le candidat certifié |
| Unicité | Clés métier locations et stations API | 200 000 / 200 000 locations ; 1 519 / 1 519 stations API | Nombre distinct = nombre total |
| Cohérence | Références stations SQL ; sommes des disponibilités ; conservation des comptes | missing_references=0 ; agrégats indépendants exacts | Zéro référence absente et égalité des agrégats |
| Exactitude | Comparaison du dernier Raw extrait aux champs non personnels Silver ; nombres et montant SQL | 200 000 lignes comparées, 0 différence ; 999 995,00 | Égalité complète et des centimes |
| Fraîcheur | Date météo J-1 exacte ; âge du flux API au gate | 4 villes au 22/10/2026 ; âge 295,97 s | 4 villes ; date attendue ; âge de -120 à 900 s |

Pour le **lot sans changements**, les populations Raw abonnés et locations sont réellement zéro. QualityRaw et QualityExact comptent donc zéro ligne et zéro défaut. Cela ne remplace pas la comparaison initiale de 200 000 lignes : les deux preuves sont conservées séparément.

Les sommes conditionnelles sur ensembles vides omettaient des champs JSON nulls. Elles ont été remplacées par countIf, qui émet des compteurs à zéro. Les seuils de certification n'ont pas été abaissés.

Le seuil de fraîcheur API de 900 secondes est une hypothèse technique configurable, pas une exigence scolaire prétendument fournie. L'âge indiqué est mesuré au démarrage de l'activité gate, à quelques instants de l'évaluation effective. La date du flux ne garantit pas qu'une station inactive ait un last_reported récent ; ces dates restent présentes pour l'analyse.

L'exactitude est relative à la source SQL de démonstration et aux calculs de rapprochement, pas à une vérité terrain indépendante. Les timestamps Raw nanosecondes sont normalisés à la microseconde pour la vérification Python de l'état Delta.

Gold final : 139 jours, 6 950 couples jour/station, 4 lignes météo, 1 519 stations API et un total de disponibilité. Sur le lot final observé : 18 863 vélos, 29 331 places, 104 stations vides et 29 pleines. Ce sont les valeurs déclarées par l'ensemble du flux ; les indicateurs peuvent être filtrés sur les drapeaux d'activité dans l'outil de restitution.
