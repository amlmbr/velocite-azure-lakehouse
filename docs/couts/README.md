# Estimation Azure — 23 octobre 2026

Estimation préparée dans **Azure Pricing Calculator**, région **Italy North**, devise **EUR**, sans modifier l'abonnement. Export déclenché vers le dossier Téléchargements du navigateur sous `ExportedEstimate (1).xlsx`. Le montant n'est pas la facture du compte étudiant.

| Poste | Hypothèse mensuelle saisie | Estimation |
|---|---|---:|
| ADF et Mapping Data Flows | 30 jours, deux démarrages de 5 min/jour, 8 vCores General Purpose, soit 5 h de cluster ; 2 milliers d'activités, 10 DIU-h, 15 h d'activités pipeline et 5 h externes | 13,46 € |
| Azure SQL | Configuration réelle Basic, 5 DTU, 2 Go inclus, une base existant 730 h | 4,31 € |
| ADLS Gen2 | Standard, Hot, LRS, namespace hiérarchique, réserve 10 Go ; 100 000 lectures/écritures, hypothèses conservatrices d'opérations et métadonnées du calculateur | 2,10 € |
| Key Vault | 1 000 opérations, aucun HSM | 0,03 € |
| Monitor | Une ressource, une série métrique d'alerte ; pas de Log Analytics supplémentaire ni notifications sortantes | 0,09 € |
| **Total affiché, arrondis du calculateur** | **Hypothèses, pas consommation mesurée** | **19,99 € / mois** |

Le calculateur utilise à cette date la conversion affichée 1 USD = 0,88 EUR. Les totaux arrondis par poste peuvent différer du total calculé sur les valeurs non arrondies.

Les 10 DIU-h provisionnées dans le calculateur couvrent les copies SQL, REST et publication : la copie SQL initiale observée facture 0,0667 DIU-h par table, même avec 14 à 18 secondes de durée. Les activités sont arrondies pour le scénario mensuel.

Le temps de cinq minutes est une hypothèse de planification, à confronter aux consommations facturables des activités. Les démarrages, échecs, reprises, temps Spark, variations régionales, volumes, conservation des snapshots et réseau peuvent augmenter le coût. Une journée sans changement SQL n'a normalement besoin que du Data Flow analytique. La base **Basic ne se met pas en pause automatiquement** : le coût subsiste quand on ferme le navigateur.

Un budget mensuel de suivi de 10 a été créé précédemment pour le groupe de ressources ; ce n'est pas un plafond bloquant et aucun destinataire d'email n'est configuré. Le scénario quotidien dépasse cette enveloppe : **le déclencheur reste arrêté**. Une enveloppe de 20–25 € serait plus prudente pour ce scénario, sous réserve des consommations réelles et sans activation implicite.

Références : https://azure.microsoft.com/en-us/pricing/calculator/ ; https://learn.microsoft.com/en-us/azure/data-factory/pricing-concepts ; https://learn.microsoft.com/en-us/azure/data-factory/apply-finops .
