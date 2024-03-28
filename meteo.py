from requests_html import HTMLSession

s = HTMLSession()


# Liste des villes à vérifier
villes = ['Briançon','Aix-en-Provence', 'Antibes', 'Cannes', 'Digne-les-Bains', 'Sisteron', 'Arles', 'Nice', 'Avignon', 'Marseille']


# Variables pour garder la trace de la ville la plus chaude
ville_chaude = ''
temp_max = -273  # Température minimale théorique, en degrés Celsius

# Boucle à travers chaque ville pour récupérer les données météo
for ville in villes:
    url = f'https://www.google.com/search?q=météo+weekend+{ville}'
    r = s.get(url, headers={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15'})
 
# Extraire la température
    
    temp = r.html.find('span#wob_tm', first=True).text
    descri = r.html.find('div.VQF4g', first=True).find('span#wob_dc', first=True).text
    if temp:
        temp = int(temp)  # Convertir la température en entier pour comparaison
        # Vérifier si cette ville est la plus chaude jusqu'à présent
        if temp > temp_max:
            temp_max = temp
            ville_chaude = ville

# Afficher la ville la plus chaude ce weekend et sa température
print(f"La ville la plus chaude de la côte d'Azur ce weekend sera : {ville_chaude} avec {temp_max}°C accompagnée de {descri}.")

