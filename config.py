

import 

import requests
from pyspark.sql.functions import *
from pyspark.sql.types import *
from notebookutils import mssparkutils



#1. Chemins d'accès Microsoft Fabric (OneLake)

WORKSPACE_NAME = "CYNA_Test_Tech"
LAKEHOUSE_NAME = "LH_Cyna"
EVENSTREAM_NAME= "ES_Logs"
EVENHOUSE_NAME= "EH_Cyna"
NOTEBOOK_NAME= "NB_Bronze"

 #Format ABFSS pour Spark 
BASE_PATH = f"abfss://{WORKSPACE_NAME}@onelake.dfs.fabric.microsoft.com/{LAKEHOUSE_NAME}.Lakehouse/Files"

PATHS = {
    "bronze": f"{BASE_PATH}/Bronze",
    "silver": f"{BASE_PATH}/Silver",
    "gold":   f"{BASE_PATH}/Gold"
}



 #2. Sources de données
SOURCES = {
    "ipsum_url": "https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt",
    "log_generator_repo": "https://github.com/cruikshank25/Security-Log-Generator"
}



#3. Paramètres de traitement (Optimisation pour 8 Go RAM)
PROCESSING_CONFIG = {
    "min_confidence_level": 3,    
    "batch_size": 50000,         
      }

