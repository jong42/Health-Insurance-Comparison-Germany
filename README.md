# Health-Insurance-Comparison-Germany

This project demonstrates how data about german health insurance fees can be scraped from the web, processed and visualized. Information about insurance fees comes from https://www.gkv-spitzenverband.de/service/krankenkassenliste/krankenkassen.jsp.

Usage:

1. Create a new Python environment
2. In that environment, run "pip install -r requirements.txt"
3. In that environment, run one of the following commands in the command line:

  - To scrape the data, navigate to hic_ger/code/data_collection and run:\
    scrapy crawl fees -O ../../data/fees.json 

  - To convert the data to csv files:\
    python ../../code/clean_data.py

  - To run the dashboard:\
    python ../../code/data_analysis/app.py


