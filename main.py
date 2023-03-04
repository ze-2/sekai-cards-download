import os
import time
import requests
from bs4 import BeautifulSoup


def parseSite():
    r = requests.get('https://www.sekaipedia.org/w/api.php?action=parse&format=json&title=Database%3ACards&prop=text&text=%7B%7BCard%20datatable%0A%7Ccharacters%20%3D%20%0A%7Cunits%20%3D%20%0A%7Csupport%20units%20%3D%20%0A%7Cattributes%20%3D%20%0A%7Crarities%20%3D%203%2C4%2CBirthday%0A%7Cstatuses%20%3D%20%0A%7Cacquire%20%3D%20%0A%7Cskills%20%3D%20%0A%7Creleased%20after%20%3D%20%0A%7Creleased%20before%20%3D%20%0A%7Ccolumns%20%3D%20%0A%7D%7D&maxage=3600&smaxage=3600',
                     headers={'Accept': 'application/json'})
    html = r.json()['parse']['text']['*']
    parsed_html = BeautifulSoup(html, features='html.parser')
    img = parsed_html.findAll('img', alt=True)
    title = []
    for x in img:
        alt_unparsed = x['alt']
        alt = alt_unparsed.replace(' thumbnail.png', '')
        alt_u = alt.replace(' ', "_")
        img_trained = alt_u + "_trained_art.png"
        img_untrained = alt_u + "_art.png"
        title.append(img_untrained)
        title.append(img_trained)

    return title


def filterLocal(unfiltered):
    os.chdir('/home/ze2/.local/share/backgrounds')
    existing = os.listdir()
    for existingCard in existing:
        unfiltered.remove(existingCard)
        if existingCard.replace("_trained_art", "") in unfiltered:
            unfiltered.remove(existingCard.replace("_trained_art", ""))
        if existingCard.replace("_art", "") in unfiltered:
            unfiltered.remove(existingCard.replace("_art", ""))
    return unfiltered


def getPicture(cardName):
    url = "https://www.sekaipedia.org/wiki/File:" + cardName
    print(url)
    page = requests.get(url).text
    html = BeautifulSoup(page, features='html.parser')
    div = html.find("a", {"class": "internal"})

    if div is None:
        newName = cardName[:len(cardName) - 8] + '.png'
        url = "https://www.sekaipedia.org/wiki/File:" + newName
        page = requests.get(url).text
        html = BeautifulSoup(page, features='html.parser')
        div = html.find("a", {"class": "internal"})
        href_unparsed_weird = div['href']
        return "https:" + href_unparsed_weird

    else:
        return "https:" + div['href']


def downloadPicture(href, cardName):
    os.chdir('/home/ze2/.local/share/backgrounds')
    response = requests.get(href)
    if response.status_code:
        fp = open(cardName, 'wb')
        fp.write(response.content)
        fp.close()
        print(response.status_code)


def main():
    cardNamesUnfiltered = parseSite()
    cardNames = filterLocal(cardNamesUnfiltered)

    for cardName in cardNames:
        href = getPicture(cardName)
        print(href)
        time.sleep(1.5)
        downloadPicture(href, cardName)
        print(cardName + " successfully downloaded!")
        print("----------------------------------------------")
    print(cardNames)


main()
