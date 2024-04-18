To use this project, follow these steps:

1. Create a Python virtual environment:

2. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

3. Install the required packages from `requirements.txt`:

4. Go to cd /jooble_scraping and run the Scrapy spider to scrape data:
```
scrapy crawl scraping_spider -O test.json

```
This command will execute the Scrapy spider named `scraping_spider` and save the output to a JSON file named `test.json`.
