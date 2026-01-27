import kagglehub
import pandas as pd
import os
import shutil
import glob

def download_and_setup_data():
    # 1. Téléchargement via l'API KaggleHub
    print("Téléchargement du dataset en cours...")
    path = kagglehub.dataset_download("pavansubhasht/ibm-hr-analytics-attrition-dataset")
    print("Chemin des fichiers téléchargés :", path)
    
    # 2. Recherche automatique de tout fichier CSV dans le dossier téléchargé
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    
    if not csv_files:
        print("Erreur : Aucun fichier CSV n'a été trouvé dans le dossier téléchargé.")
        return

    source_path = csv_files[0] # On prend le premier CSV trouvé
    print(f"Fichier trouvé : {os.path.basename(source_path)}")
    
    # 3. Destination dans votre projet (data/raw)
    destination_dir = "data/raw"
    os.makedirs(destination_dir, exist_ok=True)
    destination_path = os.path.join(destination_dir, "employees.csv")
    
    # 4. Copie et renommage
    shutil.copy(source_path, destination_path)
    print(f"Succès ! Le fichier est maintenant dans : {destination_path}")

if __name__ == "__main__":
    download_and_setup_data()