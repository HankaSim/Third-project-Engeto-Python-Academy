"""
Election_scraper.py: třetí projekt do Engeto Python Akademie

Election Scraper

author: Hana Šimečková
email: simeckova.hana8@gmail.com
discord: Hanka Š.
"""

# Importy
import sys
import os
import csv
import requests
from bs4 import BeautifulSoup as bs

# Vložený odkaz - kontrola
adresa = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
regiony_html = requests.get(adresa)
regiony_rozdeleno = bs(regiony_html.text, "html.parser")

mesta_list = []
pocet = len(regiony_rozdeleno.find_all("table", {"class": "table"}))
for cislo in range(1, pocet + 1):
    mesta_list.extend(regiony_rozdeleno.find_all("td", {"headers": f"t{cislo}sa3"}))

celky_seznam = ["https://www.volby.cz/pls/ps2017nss/" + (td_tag.a["href"])for td_tag in mesta_list]
if sys.argv[1] not in celky_seznam:
    print("Vložen nesprávný odkaz pro územní celek.")
    quit()

# Stažení a uložení dat do slovníku
def data (tr_tag, town):
    link = tr_tag.find("td", {"class": "cislo"})

    def obec_div(link_tagy):
        obec_link = link_tagy["href"]
        town_odkaz = f"https://www.volby.cz/pls/ps2017nss/{obec_link}"
        town_stranka = requests.get(town_odkaz)
        return bs(town_stranka.text, "html.parser")

# Obecná data
    def obecna_data(town_tag, link_tag):
        div_tag = obec_div(link_tag).find("div", {"id": "publikace"})
        obecne_info = div_tag.table.find_all("td")

        kod = link_tag.text
        town = town_tag.text
        volici = obecne_info[3].text
        obalky = obecne_info[4].text
        valid = obecne_info[7].text

        return {"Kód obce": kod, "Název obce": town, "Voliči": volici, "Vydané obálky": obalky, "Platné hlasy": valid}
        
# Politické strany
    def politicke_strany():
        inner = obec_div(link.a).find("div", {"id": "inner"})
        strany = [tag.text for tag in (inner.find_all("td", {"class": "overflow_name"}))]
        hlasy1 = [tag.text for tag in (inner.find_all("td", {"headers": "t1sa2 t1sb3"}))]
        hlasy2 = [tag.text for tag in (inner.find_all("td", {"headers": "t2sa2 t2sb3"}))]
        hlasy_soucet = hlasy1 + hlasy2
        hlasy = {strany[i]: hlasy_soucet[i]for i in range(len(strany))}
        return hlasy

    vysledky = {}
    vysledky.update(obecna_data(town, link.a))
    vysledky.update(politicke_strany())
    return vysledky

# Region
vlozeny_odkaz = sys.argv[1]
stranka = requests.get(vlozeny_odkaz)
region = bs(stranka.text, "html.parser")
inner = region.find("div", {"id": "inner"})
mesto = inner.find_all("tr")

# Název souboru CSV
div_topline = region.find("div", {"class": "topline"})
region_name_tag = div_topline.find_all("h3")[1]
region_raw = region_name_tag.text
region_name = region_raw.strip().lstrip("Okres: ")
soubor = f"results_{region_name}.csv"

# Kontroly argumentů
if len(sys.argv) != 3:
    print("Vložte dva argumenty pro běh programu.")
    quit()

if sys.argv[2] != soubor:
    print("Nesprávný formát druhého argumentu.")
    quit()

# Stažení dat a zapsání souboru
print("Stahování dat...")

for polozka, tr_tag in enumerate(mesto):
    mesto_tag = tr_tag.find("td", {"class": "overflow_name"})
    if mesto_tag is None:
      continue
    else:
        with open(soubor, mode="a", newline = "\n") as nove_csv:
            zahlavi = data(tr_tag, mesto_tag).keys()
            zapisovac = csv.DictWriter(nove_csv, delimiter = ";", fieldnames= zahlavi)
            if os.path.getsize(soubor) == 0:
                zapisovac.writeheader()
            else:
                zapisovac.writerow(data(tr_tag, mesto_tag))

print(f"Data uložena do souboru: {soubor}") 