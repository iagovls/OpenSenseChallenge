from bs4 import BeautifulSoup
from pathlib import Path
import datetime
import html as html_lib

def generateHTML(items):
    items = items or []
    preferred_headers = [
        "Arquivo",
        "CNPJ",
        "Resultado",
        "Número do Pedido",
        "Data do Depósito",
        "Titulo",
        "ICP",
    ]

    headers = []
    for header in preferred_headers:
        if any(isinstance(row, dict) and header in row for row in items):
            headers.append(header)

    for row in items:
        if not isinstance(row, dict):
            continue
        for key in row.keys():
            if key not in headers:
                headers.append(key)

    lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '<meta charset="utf-8">',
        "<title>PATENTES</title>",
        "</head>",
        "<body>",
        '<table border="1">',
        "<thead>",
        "<tr>",
    ]

    for header in headers:
        lines.append(f"<th>{html_lib.escape(str(header))}</th>")

    lines += [
        "</tr>",
        "</thead>",
        "<tbody>",
    ]

    for row in items:
        if not isinstance(row, dict):
            continue
        lines.append("<tr>")
        for header in headers:
            value = row.get(header, "")
            lines.append(f"<td>{html_lib.escape(str(value))}</td>")
        lines.append("</tr>")

    lines += [
        "</tbody>",
        "</table>",
        "</body>",
        "</html>",
    ]

    with open("PATENTES.HTML", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def getDate(date):
    return datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")

def getCNPJ(soup):
    textos = soup.find_all(string=True)
    for t in textos:
        if "CPF ou CNPJ do Depositante" in t:
            return t.strip()[29:-3]

def getResults(soup):
    try:
        results = soup.find("tbody", id="tituloContext").find_all("tr")
        return len(results)
    except:
        return 0

def getTableData(soup):
    results = soup.find("tbody", id="tituloContext").find_all("tr")
    for tr in results:
        print(tr.contents[5].contents[1].contents[1]) # Titulo
        print(tr.contents[1].contents[1].contents[1].contents[0].strip()) # Pedido
        print(tr.contents[7].contents[1].contents[0].strip()) # ICP
        print(tr.contents[3].contents[1].contents[0].strip()) # Data
    return title

path = Path("./PATENTES")

records = []
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
                    "Data do Depósito": getDate(tr.contents[3].contents[1].contents[0].strip()),
                    "Titulo": tr.contents[5].contents[1].contents[1].contents[0].strip(),
                    "ICP": tr.contents[7].contents[1].contents[0].strip(),
                })
        else:    
            records.append({
                "Arquivo": file.name,
                "CNPJ": getCNPJ(soup),
                "Resultado": getResults(soup),
                "Número do Pedido": "-",
                "Data do Depósito": "-",
                "Titulo": "-",
                "ICP": "-",
                    })   
       
    except Exception as e:
        print(f"Error parsing {file}: {e}")

try:
    generateHTML(records)
    print("HTML generated successfully")
except Exception as e:
    print(f"Error generating HTML: {e}")
 
