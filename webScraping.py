from collections import namedtuple
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import os

# Define a named tuple to represent article data
Article = namedtuple('Article', ['name', 'old_price', 'current_price', 'discount', 'ratings'])

def export_to_csv(article_list, csv_file_path):
    """
    Export article data to a CSV file.
    
    Args:
        article_list (list): List of named tuples representing article data.
        csv_file_path (str): File path for the CSV file.

    Returns:
        str: Success message if export is successful.
    """
    data = []
    for article in article_list:
        data.append({
            'Name': article.name,
            'Old Price': article.old_price,
            'Current Price': article.current_price,
            'Discount': article.discount,
            'Ratings': article.ratings
        })

    df = pd.DataFrame(data)
    if os.path.exists(csv_file_path):
        try:
            with open(csv_file_path, 'a', newline='') as existing_file:
                df.to_csv(existing_file, header=False, index=False)
            return 'New information added successfully'
        except Exception as e:
            print("An error occurred:", e)
    else:
        df.to_csv(csv_file_path, index=False)
        return 'Information exported successfully'


def find_articles(mercado_articles):
    """
    Find and extract article data from Mercado Libre articles.

    Args:
        mercado_articles (list): List of BeautifulSoup elements representing articles.

    Returns:
        list: List of named tuples containing article data.
    """
    articles_list = []
    for article in mercado_articles:
        name = article.find('h2', class_='ui-search-item__title').text
        old_price = article.find('span', class_='andes-money-amount__fraction').text.replace('.', '')
        current_price = article.find('span', class_='andes-money-amount__fraction').text.replace('.', '')
        discount = article.find('span', class_='ui-search-price__discount shops__price-discount')
        ratings = article.find('span', class_='ui-search-reviews__amount')

        if discount is not None:
            discount = discount.text
        else:
            discount = 'No discount'

        if ratings is not None:
            ratings = ratings.text
        else:
            ratings = 'No ratings available'

        article_data = Article(name, old_price, current_price, discount, ratings)
        articles_list.append(article_data)

    return articles_list


def select_article(art):
    """
    Select the URL for a specific article type or category.

    Args:
        art (str): Article type or category.

    Returns:
        str: URL for the specified article type or category.
    """
    website_url = f'https://listado.mercadolibre.com.co/{art}#D[A:celular]'
    return website_url


def select_page(page):
    """
    Select the URL for a specific page number.

    Args:
        page (str): Page number.

    Returns:
        str: URL for the specified page number.
    """
    page_url = f'https://listado.mercadolibre.com.co/celulares-telefonos/celulares-smartphones/celulares_Desde_' \
               f'{page}_NoIndex_True'
    return page_url


# Select article and page
article_url = select_article('cell-phones')  
page_url = select_page('51')  

# Make a GET request to the article URL and get HTML content
html_text = requests.get(page_url).text  
# Create a BeautifulSoup instance to parse HTML content
soup = BeautifulSoup(html_text, 'html.parser')
# Find and extract all <li> elements with the specified class
articles = soup.find_all('li', class_='ui-search-layout__item shops__layout-item ui-search-layout__stack')

# Execute
mercado_articles = find_articles(articles)

# Get the directory of the current script file
script_dir = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join(script_dir, 'cell_phones.csv')

# Save
export_to_csv(mercado_articles, csv_file_path)
