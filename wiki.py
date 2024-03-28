import requests
from bs4 import BeautifulSoup
import pandas as pd

######## 1.URL de la page Wikipedia avec le classement des aéroports ##########
url = 'https://fr.wikipedia.org/wiki/Liste_des_a%C3%A9roports_les_plus_fr%C3%A9quent%C3%A9s_en_France'
# Faire une requête GET pour récupérer le contenu de la page
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers)

# Vérifier que la requête a réussi
if response.status_code == 200:
    # Utilisation de BeautifulSoup pour parser le HTML de la page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Recherche du premier tableau de la page, qui contient les données d'intérêt
    table = soup.find_all('table', {'class': 'wikitable'})[0]
    
    # Initialisation d'une liste pour stocker les données des aéroports
    data = []
    
    # Extraction des données et des URL des 10 premières lignes du tableau
    rows = table.find_all('tr')[1:11]  # Ignorer l'en-tête du tableau et se limiter aux 10 premiers
    for row in rows:
        cols = row.find_all('td')
        if cols:
            rang = cols[0].text.strip()
            aeroport = cols[1].text.strip()
            code_iata = cols[2].text.strip()
            passagers_2022 = cols[5].text.strip().replace('\xa0', ' ')  # Remplacer les espaces insécables
            
            # Extraire l'URL de l'aéroport
            aeroport_link = cols[1].find('a', href=True)
            if aeroport_link:
                aeroport_url = "https://fr.wikipedia.org" + aeroport_link['href']
            else:
                aeroport_url = "N/A"
            
            data.append([rang, aeroport, code_iata, passagers_2022, aeroport_url])
    
    # Conversion des données en DataFrame pandas
    df = pd.DataFrame(data, columns=['Rang', 'Aéroport', 'Code IATA', 'Nombre de passager', 'URL'])
    
else:
    print(f"Échec de la requête: statut {response.status_code}")


########### 2. Coordonnées géographiques ########

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

for indice, row in df.iterrows():
    aeroport_url = row['URL']
    if aeroport_url != "N/A":
        response = requests.get(aeroport_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Trouver le lien qui contient les coordonnées géographiques
            coord_link = soup.find('a', {'class': 'mw-kartographer-maplink'})
            if coord_link and 'data-lat' in coord_link.attrs and 'data-lon' in coord_link.attrs:
                lat = coord_link['data-lat'].strip()
                lon = coord_link['data-lon'].strip()
                df.at[indice, 'Latitude'] = lat
                df.at[indice, 'Longitude'] = lon






############  3. Déstinations desservit ##########

# Charger le DataFrame à partir du fichier CSV
base_donnee = pd.read_csv('base_donnee.csv')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_destinations(url):
    """
    Fonction pour récupérer les compagnies aériennes et leurs destinations
    à partir de l'URL de la page Wikipedia de chaque aéroport.
    """
    compagnies = []
    destinations = []
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Trouver le tableau contenant les informations sur les compagnies et les destinations
        table = soup.find('table', class_='wikitable sortable alternance collapsible')
        
        if table:
            for row in table.find_all('tr')[1:]:  # Ignorer l'en-tête du tableau
                cells = row.find_all('td')
                if len(cells) >= 2:  # Assurer que la ligne contient au moins deux cellules
                    compagnie = cells[0].get_text(strip=True)
                    destination_list = cells[1].find_all('a')
                    destination_names = [dest.get_text(strip=True) for dest in destination_list]
                    
                    compagnies.append(compagnie)
                    destinations.append(", ".join(destination_names))
                    
    return compagnies, destinations

# Itérer sur chaque ligne du DataFrame pour récupérer et ajouter les informations
for index, row in base_donnee.iterrows():
    compagnies, destinations_list = get_destinations(row['URL'])
    base_donnee.at[index, 'Compagnies'] = "; ".join(compagnies)
    base_donnee.at[index, 'Destinations'] = "; ".join(destinations_list)







# Chargement du DataFrame existant
base_donnee = pd.read_csv('base_donnee.csv')

# URL pour l'aéroport de Paris-Charles de Gaulle
url_cdg = 'https://fr.wikipedia.org/wiki/Destinations_au_d%C3%A9part_de_Paris-Charles-de-Gaulle'

# Initialisation des en-têtes de la requête HTTP
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Requête HTTP GET
response = requests.get(url_cdg, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Sélecteur pour trouver le tableau des destinations
    table = soup.find('table', class_='wikitable sortable alternance collapsible')
    
    if table:
        compagnies_destinations = []
        tbody = table.find('tbody')
        if tbody:
            for tr in tbody.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) >= 2:  # Vérifier qu'il y a au moins deux td (compagnie + destinations)
                    compagnie_aerienne = tds[0].text.strip()
                    destinations = [a.text.strip() for a in tds[1].find_all('a')]
                    compagnies_destinations.append((compagnie_aerienne, ', '.join(destinations)))
        
        # Supposer que vous voulez ajouter ces informations à la première ligne correspondant à Paris-Charles de Gaulle dans 'base_donnee'
        index_cdg = base_donnee[base_donnee['Aéroport'] == 'Paris-Charles de Gaulle'].index[0]
        base_donnee.at[index_cdg, 'Compagnies'] = '; '.join([cd[0] for cd in compagnies_destinations])
        base_donnee.at[index_cdg, 'Destinations'] = '; '.join([cd[1] for cd in compagnies_destinations])
    else:
        print("Tableau des destinations non trouvé.")
else:
    print(f"Échec de la requête HTTP: statut {response.status_code}")

# Sauvegarder les modifications dans un nouveau fichier CSV
base_donnee.to_csv('base_donnee_mise_a_jour.csv', index=False)
