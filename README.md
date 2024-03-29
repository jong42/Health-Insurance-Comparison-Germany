# Health-Insurance-Comparison-Germany (HIC_Ger)

This project demonstrates how data about german health insurance fees can be scraped from the web, processed and visualized. Information about insurance fees comes from https://www.gkv-spitzenverband.de/service/krankenkassenliste/krankenkassen.jsp. Geojson file for cartographic visualizations is taken from https://github.com/isellsoap/deutschlandGeoJSON.

Usage:

1. Create a new Python environment (Python 3.8 or newer)
2. In that environment, run "pip install -r requirements.txt"
3. In that environment, run one of the following commands in the command line:

  - To scrape the data, navigate to hic_ger/data_collection and run:\
    scrapy crawl fees -O ../data/fees.json 

  - To convert the data to csv files:\
    python hic_ger/clean_data.py

  - To run the dashboard:\
    python hic_ger/app.py


