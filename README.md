# Mercado Libre Article Scraper

## Introduction
This Python script is designed to scrape article data from Mercado Libre, a popular online marketplace. It utilizes web scraping techniques to extract information about cell phones, including their names, prices, discounts, and ratings.

## Requirements
To run this script, you need to have the following Python libraries installed:
- `collections`
- `bs4` (Beautiful Soup)
- `selenium`
- `requests`
- `pandas`
- `os`

You can install these libraries using pip:
```bash
pip install collections bs4 selenium requests pandas
```

## Usage
Clone the Repository: Clone or download this repository to your local machine.
Install Dependencies: Ensure you have installed all the required dependencies as mentioned above.
Run the Script: Execute the Python script webScraping.py in your preferred Python environment.
Output: The script will scrape article data from Mercado Libre and export it to a CSV file named cell_phones.csv.

## Script Details
### Functions
export_to_csv(article_list, csv_file_path): Exports article data to a CSV file.
find_articles(mercado_articles): Finds and extracts article data from Mercado Libre articles.
select_article(art): Selects the URL for a specific article type or category.
select_page(page): Selects the URL for a specific page number.

## Note
The script may require adjustments based on changes in the Mercado Libre website structure.
