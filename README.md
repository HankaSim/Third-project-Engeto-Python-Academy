# Election scraper
### **Třetí projekt pro Engeto Python Academy**
#

### **Popis programu**
Program umožňuje stáhnout a uložit vybraná data volebních výsledků z roku 2017: 
[Výsledky voleb 2017](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ "Výsledky voleb 2017")

### **Spuštění programu**
Potřebné instalace jsou shrnuty v souboru **requirements.txt**.
Program se spouští pomocí dvou argumentů:
* Odkaz na zvolený volební okrsek (Zvolené město) po kliknutí na "X" ve sloupci "Výběr obce"
* Druhý argument ve formátu "results_Zvolené město.csv"

### **Běh programu**
**_Ukázka pro okrsek Uherské Hradiště:_**

PS C:\Users\simec\Desktop\Elections_scraper> python Elections_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7202" "results_Uherské Hradiště.csv"

Stahování dat...

Data uložena do souboru: results_Uherské Hradiště.csv






