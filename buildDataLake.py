import requests
import zipfile
import io
import os
import shutil
from kaggle.api.kaggle_api_extended import KaggleApi

def getDataWorldCsv(api_url: str, token: str, output_path: str) -> str:
    """ Get File from data.world """
    try : 
        headers = {
            'Authorization': f"Bearer {token}"
        }

        # Faire la requête HTTP GET à l'API
        response = requests.get(api_url, headers=headers)

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Ouvrir un fichier binaire pour écrire la réponse
            zip_file_path = os.path.join(output_path, 'data.zip')
            with open(zip_file_path, 'wb') as file:
                file.write(response.content)

            # Utiliser io.BytesIO pour lire le fichier zip en mémoire
            zip_data = io.BytesIO(response.content)

            # Ouvrir le fichier zip en mémoire
            with zipfile.ZipFile(zip_data, 'r') as zip_ref:
                # Extraire tout dans un répertoire temporaire
                temp_extract_path = os.path.join(output_path, 'temp_extracted')
                zip_ref.extractall(temp_extract_path)
                
                # Trouver le fichier CSV dans le répertoire temporaire et ses sous-dossiers
                for root, dirs, files in os.walk(temp_extract_path):
                    for filename in files:
                        if filename.endswith('.csv'):
                            # Construire le chemin complet du fichier source et de destination
                            source_file = os.path.join(root, filename)
                            destination_file = os.path.join(output_path, filename)
                            
                            # Déplacer le fichier CSV dans le dossier racine
                            shutil.move(source_file, destination_file)
                            
                # Supprimer le fichier zip et le répertoire temporaire
                os.remove(zip_file_path)
                shutil.rmtree(temp_extract_path)
                
                return "Les fichiers CSV ont été déplacés avec succès dans le dossier racine."
        else:
            return f"La requête a échoué avec le code d'état: {response.status_code}"
    except Exception as e:
        print("Une erreur est survenue: ", str(e))
        return "Une erreur lors du téléchargement du dataset. "



def getKaggleCsv(api_authentification : KaggleApi, output_path : str) -> str :
    """ Get File from kaggle """
    try : 
        api_authentification.authenticate()

        # Téléchargez un dataset spécifique
        datasets = ['gregorut/videogamesales', 'sidtwr/videogames-sales-dataset', 'rankirsh/evolution-of-top-games-on-twitch']
        # Remplacez 'dataset-owner/dataset-name' par le chemin du dataset que vous souhaitez télécharger
        for dataset in datasets :
            api_authentification.dataset_download_files(dataset, path=output_path, unzip=True)

        return 'Le(s) dataset(s) provenant de kaggle a/ont été téléchargé(s) et dézippé(s).'
    except Exception as e:
        print("Une erreur est survenue: ", str(e))
        return "Le dataset n'a pas été téléchargé et dézippé."


######################### EXECUTE #####################################
# Remplacez 'API_ENDPOINT' par l'URL de l'API et 'YOUR_TOKEN_HERE' par votre token d'API ainsi que le chemin d'extraction
API_DATAWORLD = "https://api.data.world/v0/download/yansian/popular-video-games"
TOKEN_DATAWORLD = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJwcm9kLXVzZXItY2xpZW50OnJhemFmeSIsImlzcyI6ImFnZW50OnJhemFmeTo6YWZmZGUxMzUtNDVlNi00NTk5LWFlOWQtMGI5MjhhMTZiZmNlIiwiaWF0IjoxNzA4MzM5MDUwLCJyb2xlIjpbInVzZXJfYXBpX3JlYWQiLCJ1c2VyX2FwaV93cml0ZSJdLCJnZW5lcmFsLXB1cnBvc2UiOnRydWUsInNhbWwiOnt9fQ.WepLPSNrzn2eGURLA_yvGRCxpV0nn8fsTrH71KfTBrnheFKFUfxpQgRmbhZZiyP1N9-LWFWthHFywX7LUdfYyA"

API_KAGGLE = KaggleApi()
path_to_extract = "C:/Users/EXEIO/Desktop/sup_de_vinci/cours/datawarehouse/dataset"

print(getDataWorldCsv(API_DATAWORLD, TOKEN_DATAWORLD, path_to_extract))
print(getKaggleCsv(API_KAGGLE, path_to_extract))
