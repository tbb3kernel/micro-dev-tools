from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import csv
from datetime import datetime

# TODO: 1. All the information actually contains in `header_rows: list[Tag]`
# TODO: 2. Create logging functionality
# TODO: 3. Re-structure code to be CLI program


YC_NEWS_URL: str = "https://news.ycombinator.com/"


def get_html_content(url: str) -> str:
    """Fetches the HTML content from the given URL.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content as a string, or None if an error occurred.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to get response from {url}")
        return None


def parse_news_data(html_content: str) -> tuple[list[str], list[str]]:
    """Parses the HTML content to extract header and meta information from the news table.

    Args:
        html_content: The HTML content to parse.

    Returns:
        A tuple containing two lists: header_rows and meta_rows.
        Returns empty lists if no news data is found.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    news_table = soup.find('table')

    if not news_table:
        print("Could not find news table")
        return [], []

    print("Found news table...")
    rows = news_table.find_all('tr')

    if not rows:
        print("Could not find news rows")
        return [], []

    print(f"Found {len(rows)} news items")
    header_rows: list = []
    meta_rows: list = []

    for i in range(0, len(rows), 3):
        if i + 1 < len(rows):  # makes sure there is a meta row
            header_row = rows[i]
            meta_row = rows[i + 1]
            header_rows.append(header_row)
            meta_rows.append(meta_row)

    # filter out empty strings
    header_rows = list(filter(None, header_rows))
    meta_rows = list(filter(None, meta_rows))

    return header_rows, meta_rows


def print_news_items(header_rows: list[str], meta_rows: list[str]) -> None:
    """Prints the news items to the console.

    Args:
        header_rows: The list of header rows.
        meta_rows: The list of meta rows.
    """
    print("Printing news items...")
    for header, meta in zip(header_rows, meta_rows):
        print(f"\n{header}\t-\t{meta}\n")


def save_news_to_csv(header_rows: list[str], meta_rows: list[str], filename: str) -> None:
    """Saves the news data to a CSV file.

    Args:
        header_rows: The list of header rows.
        meta_rows: The list of meta rows.
        filename: The name of the CSV file to create.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["header", "meta"])
        for header, meta in zip(header_rows, meta_rows):
            writer.writerow([header, meta])
    print(f"News data saved to {filename}")


def get_url_from_news_element(news_element: Tag) -> str:
    news_url: str = news_element['href']
    return news_url


def get_title_from_news_element(news_element: Tag) -> str:
    news_title: str = news_element.text.strip()
    return news_title

def get_metadata_from_element(meta_element: Tag) -> tuple[str, str]:
    pass


def main():
    """Main function to orchestrate the news fetching and processing."""
    html_content = get_html_content(YC_NEWS_URL)
    if html_content:
        header_rows, meta_rows = parse_news_data(html_content)
        print(header_rows[1])
        if header_rows and meta_rows:
            # print_news_items(header_rows, meta_rows)

            # Save to CSV (optional)
            now = datetime.now()
            dt_string = now.strftime("%Y%m%d_%H%M%S")
            filename = f"yc_news_{dt_string}.csv"
            # You can uncomment below line if you always want to save to csv
            # save_news_to_csv(header_rows, meta_rows, filename)


if __name__ == '__main__':
    main()
