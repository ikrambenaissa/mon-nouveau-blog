import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la page contenant les informations sur les compagnies aériennes
url = 'https://www.wego.fr/aeroports/fr/aeroports-en-france'

# Faire une requête GET pour récupérer le contenu de la page
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Analyser le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraire les informations sur les compagnies aériennes
    airlines = []
    for li in soup.select('.airlines-in-location li'):
        # Nom de la compagnie aérienne
        name = li.find('a').get_text(strip=True)
        # Code IATA de la compagnie aérienne (s'il est présent)
        code = li.find('span').get_text(strip=True) if li.find('span') else ''
        # URL du logo
        logo_url = li.find('img')['src'] if li.find('img') else ''
        
        airlines.append({'Compagnie Aérienne': name, 'Code IATA': code, 'Logo URL': logo_url})

    # Créer un DataFrame à partir de la liste des compagnies aériennes
    df_airlines = pd.DataFrame(airlines)
    
    # Afficher le DataFrame
    #print(df_airlines)
    
    # Sauvegarder le DataFrame dans un fichier CSV
    df_airlines.to_csv('compagnies_aeriennes_france.csv', index=False)
else:
    print(f"Erreur lors de la requête HTTP : code {response.status_code}")
