import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


url = 'https://bnf.nice.org.uk/interaction/'

r = requests.get(url, 'html.parser')

html_contents = r.text

html_soup = BeautifulSoup(html_contents, features="html.parser")

links = []

for i in html_soup.find_all('a'):
    links.append(i.get('href'))

# 29:-1 is the maximum of all links
links = links[29:-1]

urls = []

for i in links:
    urls.append(url + str(i))

# urls = urls[399:402]

# r = requests.get('https://bnf.nice.org.uk/interaction/adefovir.html', 'html.parser')

# r = requests.get('https://bnf.nice.org.uk/interaction/abacavir-2.html', 'html.parser')


def INTERACTIONS(r):

    html_contents = r.text

    html_soup = BeautifulSoup(html_contents, features="html.parser")

    div = []

    for i in html_soup.find_all('div'):
        div.append(i)

    info = []
    Info = []
    newInfo = []

    for i in div:
        if 'Useful information' in i.text:
            Info.append(i.text)
        if 'has the following interaction information:' in i.text:
            info.append(i.text)

    for j in Info:
        newInfo.append(j)
    for j in info:
        newInfo.append(j)

    newInfo = re.sub(r'\n+', '\n', newInfo[0])

    newInfo = newInfo.split('Useful information', 1)

    info0 = newInfo[0].split('\n')

    info0 = list(filter(None, info0))

    info1 = info[1].split('\n')

    # Capture Interactions here **************************************************************
    idx = info1.index('            has the following interaction information:')
    # print(info1[1])
    Name = info1[1].strip()
    # print(Name)

    # Name = Name[0]

    idx = []
    for i in info0:
        idx.append(info1.index(i))

    data = [info1[i: j] for i, j in zip(idx, idx[1:] + [None])]

    dic = {}

    dic[Name] = {}

    for i in data:

        if 'Severity of interaction:' in i:

            dic[Name][i[0]] = i[i.index('Severity of interaction:') + 1]

        else:

            dic[Name][i[0]] = 'Unknown'

    return pd.DataFrame(dic)


data = []

# p0 = data.append(INTERACTIONS(urls))


for i in urls:
    r = requests.get(i, 'html.parser')

    data.append(INTERACTIONS(r))

p = pd.concat(data, axis=1)

p.to_csv('drug-capture-test.csv')






