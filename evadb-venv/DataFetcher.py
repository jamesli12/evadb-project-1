import requests
from bs4 import BeautifulSoup
import re

class DataFetcher:

    def get_data(self, company, news_type):
        data = []

        uri = f"https://google.com/search?q={company}%20Company%20{news_type}%20News"
        res = requests.get(uri)
        soup = BeautifulSoup(res.text, "html.parser") 
        heading_object = soup.find_all('h3') 
        for info in heading_object: 
            formatted_str = re.sub(r'\W+', ' ', info.getText()).strip()
            data.append(bytes(formatted_str, 'utf-8').decode('utf-8', 'ignore'))
        return data