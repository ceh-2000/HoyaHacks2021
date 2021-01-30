from bs4 import BeautifulSoup
import requests

def get_meats(url):
    #Nab the HTML data
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'html.parser')

    #Grab out the site text
    all_text_list = soup.find_all('li')
    all_text_ish = ' '.join([t.text for t in all_text_list]).replace('\n', ' ')

    #Look for meat occurences
    meat_words = ['chicken', 'beef', 'ham', 'meat', 'pork', 'salami', 'turkey', 'steak', 'sausage']
    new_meats = sum([all_text_ish.count(m) for m in meat_words])

    return new_meats

if __name__ == '__main__':
    print(get_meats('https://www.foodnetwork.com/recipes/food-network-kitchen/moroccan-meatball-soup-3721438'))
