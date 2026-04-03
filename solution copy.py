from bs4 import BeautifulSoup
from pathlib import Path
import datetime



file = "./PATENTES/00001180000126-01.html"
with open(file, "r", encoding="ISO-8859-1") as file:
        html = file.read()
        soup = BeautifulSoup(html, "html.parser")
        results = soup.find("tbody", id="tituloContext")#.find_all("tr")
        print(results)
        # for tr in results:
        #     print(tr.contents[5].contents[1].contents[1].contents[0].strip())
                      
