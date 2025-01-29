from bs4 import BeautifulSoup
import requests

YC_NEWS_URL: str = "https://news.ycombinator.com/"

response = requests.get(YC_NEWS_URL)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    news_table = soup.find('table')
    if not news_table:
        print("Could not find news table")
        # exit(1)
    # print(news_table.prettify())
    print("Found news table...")
    rows = news_table.find_all('tr')
    if not rows:
        print("Could not find news rows")
        exit(1)
    print("Found news rows...")
    print(f"Found {len(rows)} news items")
    header_rows: list = []
    meta_rows: list = []
    for i in range(0, len(rows), 3):
        header_row = rows[i]
        meta_row = rows[i+1]
        # I personally don't use this row (empty row for spacing)
        # _skip_row = rows[i+2]
        header_rows.append(header_row.text.strip())
        meta_rows.append(meta_row.text.strip())

    # filter out empty strings
    header_rows = list(filter(None, header_rows))
    meta_rows = list(filter(None, meta_rows))

    print("Printing news items...")
    for header, meta in zip(header_rows, meta_rows):
        print(f"\n{header}\t-\t{meta}\n")

    # save to csv format
    import csv
    from datetime import datetime
    now = datetime.now()
    # define date format as you like
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    filename = f"yc_news_{dt_string}.csv"
    write_flag: bool = False
    if write_flag:
        with open(filename, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(["header", "meta"])
            meta_regex = ".*news.*"
            for header, meta in zip(header_rows, meta_rows):
                writer.writerow([header, meta])
