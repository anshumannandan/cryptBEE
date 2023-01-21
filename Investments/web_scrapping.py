import requests
from bs4 import BeautifulSoup
import base64

def web_scrap_news():

    url = 'https://cryptopotato.com/crypto-news/'
    requestcontent = requests.get(url)
    htmlcontent = requestcontent.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')

    newslist = []

    for u_list in soup.find_all('li' ,class_='rpwe-li'):
        for list_element in u_list.contents:
            for tag in list_element:
                try:
                    # get src
                    src = tag.get('src')
                    # get src in decrypyted base64
                    svg_src = base64.b64decode(src.split('base64,')[1])
                    # get image src from decrypted base64 src
                    html_src = str(svg_src).split('data-u="')[1].split('" data-w')[0]
                    # html decrpytion
                    html_src = html_src.replace('%3A',':')
                    html_src = html_src.replace('%2F','/')
                    # html_src has decrypted image src
                    image_url = html_src
                except:
                    try:
                        news_link = tag.get('href')
                        news_headline = tag.string
                    except:
                        pass
        newslist.append([news_headline, news_link, image_url])

    return newslist