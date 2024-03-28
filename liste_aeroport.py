import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL du site contenant les informations sur les aéroports
url = 'https://www.wego.fr/aeroports'

# Faire une requête GET pour récupérer le contenu de la page
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url,  headers=headers)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Utiliser BeautifulSoup pour analyser le contenu HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trouver tous les éléments 'a' dans la liste des aéroports
    airport_links = soup.select('.popular-airports li a')
    
    # Extraire et afficher les noms des aéroports
    airports = [link.get_text(strip=True) for link in airport_links]
    aeroport_fr = pd.DataFrame(airports, columns = ['Aéroport'])
    #print(aeroport_fr)
else:
    print(f"Échec de la requête HTTP : code de statut {response.status_code}")


import requests

def get_airport_coordinates(airport_name):
    search_query = airport_name.replace(' ', '+')
    url = f"https://nominatim.openstreetmap.org/search?q={search_query}&format=json&limit=1"

    response = requests.get(url)
    if response.status_code == 200 and response.json():
        results = response.json()[0]
        return results["lat"], results["lon"]
    else:
        return None, None

# Initialiser deux listes vides pour stocker les latitudes et longitudes
latitudes = []
longitudes = []

# Parcourir chaque aéroport dans la DataFrame
for airport_name in aeroport_fr['Aéroport']:
    lat, lon = get_airport_coordinates(airport_name)
    latitudes.append(lat)
    longitudes.append(lon)

# Ajouter les latitudes et longitudes à la DataFrame
aeroport_fr['Latitude'] = latitudes
aeroport_fr['Longitude'] = longitudes

# Afficher la DataFrame mise à jour
#print(aeroport_fr)

# Sauvegarder le DataFrame dans un fichier CSV sans inclure l'index du DataFrame
aeroport_fr.to_csv('aeroports.csv', index=True)
