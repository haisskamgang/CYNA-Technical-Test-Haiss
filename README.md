# Test Technique Data Engineer - CYNA
Ce projet implémente un pipeline de données pour l'analyse de logs de sécurité en temps réel.
## Choix Architecturaux : Architecture en Médaillon
J'ai organisé les données en trois couches pour garantir la performance et la qualité :
- **Bronze** : Données brutes issues du générateur de logs et d'IPSUM.
- **Silver** : Nettoyage et **enrichissement**. C'est ici que je joins les logs avec les IPs malveillantes.
- **Gold** : Tables agrégées pour Power BI (KPIs par protocole, sévérité et heure).
## KPI du Dashboard
Le dashboard permet de répondre aux questions suivantes :
- Quels sont les protocoles les plus vulnérables ?
- Quelle est l'évolution horaire des événements critiques ?
- Quel est le ratio d'événements malveillants par rapport au trafic total ?

  ##  Comment lancer la solution

ces étapes permetent de  configurer et exécuter le pipeline de données sur votre environnement :

### 1. Prérequis
*Intaller Azure- -eventhub
*Installer python-dotenv pYyaml
* Un espace de travail (Workspace) **Microsoft Fabric**.
* Un **Lakehouse** configuré avec les dossiers Bronze, Silver et Gold.
* Python 3.14+ (si vous exécutez les scripts d'ingestion localement).

### 2. Configuration de la solution
 il faut adapter les parametres a l'environement avant de lancer la solution :
1.  Ouvrir le fichier config.py.
2.  Modifier la variable BASE_PATH pour qu'elle pointe vers l'identifiant ABFSS de votre Lakehouse.

### 3. Exécution du Pipeline (Architecture Medallion)
L'exécution se fait de manière global dans un seul notebook

1.  **Ingestion (Bronze)** : Lancer le Notebook NB_Bronze. Il récupère les logs en temps réel et le flux IPSUM pour les stocker
3.  **Agrégation (Gold)** : Lancer le Notebook NB_Bronze. lancer le LakeHouse "LH_CYNA" conteneat toute les tables
### 4. Visualisation des données
1.  Télécharger le fichier Security_Dashboard.pbix présent dans le dossier dashboards.
2.  Ouvrez-le avec **Power BI Desktop**.
3.  Cliquez sur **Actualiser** pour lier le rapport à vos tables Gold fraîchement générées.
   
##  Fontionnalités
- **Ce qui fonctionne** : L'ingestion automatisée et la détection des IPs malveillantes, pepiline automatise, flux de données, envoie deslogs, dashboard interactifs
- **Difficultés** : connecter mon evenstream au evenhouse, creer une jointure entre la base de données KQL et le lakehouse.
- **Compromis** : J'ai filtré uniquement les IPs dans IPSUM pour optimiser la jointure
