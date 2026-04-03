from bs4 import BeautifulSoup
from pathlib import Path
import datetime

# Gera um arquivo PATENTES.html com os dados dos registros em items
# items: uma lista de dicionários, cada um representendo um registro com os campos:
#   Arquivo: nome do arquivo html
#   CNPJ: CNPJ
#   Resultado: quantidade de resultados encontrados em cada arquivo
#   Número do Pedido: número do pedido
#   Data do Depósito: data do depósito
#   Título: título da patente
#   ICP: número do ICP
def generateHTML(items):

    lines = ""

    for d in items:
        lines += f"<tr><td>{d['Arquivo']}</td><td>{d['CNPJ']}</td><td>{d['Resultado']}</td><td>{d['Número do Pedido']}</td><td>{d['Data do Depósito']}</td><td>{d['Título']}</td><td>{d['ICP']}</td></tr>"

    html = f"""
    <html>
    <head>
        <style>
            table {{
                border-collapse: collapse;
                margin-left: auto;
                margin-right: auto;
                text-align: center;
            }}
            th, td {{
                padding: 10px;
            }}
        </style>
    </head>
    <body>
        <table border="1">
            <tr><th>Arquivo</th><th>CNPJ</th><th>Resultado</th><th>Número do Pedido</th><th>Data do Depósito</th><th>Título</th><th>ICP</th></tr>
            {lines}
        </table>
    </body>
    </html>
    """

    with open("PATENTES.html", "w", encoding="utf-8") as file:
        file.write(html)

# Formata a data para o formato YYYY-MM-DD
def formatDate(date):
    return datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")

# Retorna o CNPJ do arquivo html
# Busca todos os elementos de texto e retorna uma substring do primeiro elemento que contém "CPF ou CNPJ do Depositante"
# Se não encontrar, retorna "-"
def getCNPJ(soup):
    textos = soup.find_all(string=True)
    for t in textos:
        if "CPF ou CNPJ do Depositante" in t:
            return t.strip()[29:-3]
    return "-"

# Retorna a quantidade de resultados encontrados no arquivo html

def getResults(soup):
    try:
        results = soup.find("tbody", id="tituloContext").find_all("tr")
        return len(results)
    except:
        return 0

path = Path("./PATENTES")

records = []

# Processa todos os arquivos html na pasta PATENTES
for file in path.glob("*.html"):
    with open(file, "r", encoding="ISO-8859-1") as htmlFile:
        html_content = htmlFile.read()

    try:
        soup = BeautifulSoup(html_content, "html.parser")
        resultado = getResults(soup)
        if resultado != 0:
            results = soup.find("tbody", id="tituloContext").find_all("tr")
            for tr in results:
                records.append({
                    "Arquivo": file.name,
                    "CNPJ": getCNPJ(soup),
                    "Resultado": getResults(soup),
                    "Número do Pedido": tr.contents[1].contents[1].contents[1].contents[0].strip(),
                    "Data do Depósito": formatDate(tr.contents[3].contents[1].contents[0].strip()),
                    "Título": tr.contents[5].contents[1].contents[1].contents[0].strip(),
                    "ICP": tr.contents[7].contents[1].contents[0].strip(),
                })
        else:    
            # Se não encontrar resultados, adiciona um registro com os campos preenchidos com "-"
            records.append({
                "Arquivo": file.name,
                "CNPJ": getCNPJ(soup),
                "Resultado": getResults(soup),
                "Número do Pedido": "-",
                "Data do Depósito": "-",
                "Título": "-",
                "ICP": "-",
                    })   
       
    except Exception as e:
        print(f"Error parsing {file}: {e}")

try:
    generateHTML(records)
    print("HTML generated successfully")
except Exception as e:
    print(f"Error generating HTML: {e}")
 
