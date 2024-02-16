import csv
import os
from serpapi import GoogleSearch

def extraire_dentistes(params, fichier_csv, page_limit=5):
    # Vérifie si le fichier existe déjà et s'il est vide pour ajouter les en-têtes
    fichier_existe = os.path.exists(fichier_csv)
    ajouter_entetes = not fichier_existe or os.stat(fichier_csv).st_size == 0

    page = 0
    while page < page_limit:
        search = GoogleSearch(params)
        data = search.get_dict()
        results = data.get('local_results', [])
        
        with open(fichier_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Ajoute les en-têtes uniquement si nécessaire
            if ajouter_entetes:
                writer.writerow(["Nom", "Adresse", "Téléphone", "Site web"])
                ajouter_entetes = False  # S'assure que les en-têtes ne sont ajoutés qu'une fois

            for result in results:
                nom = result.get('title', 'N/A')
                adresse = result.get('address', 'N/A')
                telephone = result.get('phone', 'N/A')
                site_web = result.get('website', 'N/A')
                writer.writerow([nom, adresse, telephone, site_web])

        print(f"Page {page + 1} traitée.")
        page += 1
        params['start'] = page * 20  # Mise à jour du décalage pour la pagination

# Paramètres initiaux pour la recherche
params = {
    "engine": "google_maps",
    "q": "dentiste OR tandarts OR Zahnart",
    "ll": "@51.1174852,4.862024,12.17z",
    "type": "search",
    "hl": "fr",
    "gl": "be",
    "google_domain": "google.be",
    "api_key": "Votre_clef_api_serpapi"
}

fichier_csv = 'dentistes_belgique.csv'
extraire_dentistes(params, fichier_csv)
