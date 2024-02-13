from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def scrape_table(url):
    # Start a new instance of Chrome webdriver
    driver = webdriver.Chrome()

    # Navigate to the URL
    driver.get(url)

    try:
        # Wait for the table to be loaded (adjust the timeout as needed)
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'rows-striped'))
        )

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the tbody element with the specified class
        tbody = soup.find('tbody', class_='rows-striped text-right')

        # Check if the tbody exists
        if tbody:
            # Find all rows within the tbody
            rows = tbody.find_all('tr')

            # Initialize an empty list to store the scraped data
            data = []

            # Iterate through each row and extract the data
            for row in rows:
                # Find all cells within the row
                cells = row.find_all('th') + row.find_all('td')
                # Extract text from each cell and append to the data list
                row_data = [cell.get_text() for cell in cells]
                data.append(row_data)

            return data
        else:
            print("Table body not found on the page.")
    finally:
        # Close the webdriver
        driver.quit()


# All $1 entry scratch off Lottery ID's
oneEntry = ["7026", "7024", "5050", "5044", "5032", "5022", "1551", "1544", "1540",
            "1536", "1525", "1515", "1506", "1502", "1496", "1466", "1459"]
for gameID in oneEntry:
    url = 'https://floridalottery.com/games/scratch-offs/view?id=' + str(gameID)
    scraped_data = scrape_table(url)
    if scraped_data:
        TotalExpectedValue = 0
        pXTotal = 0
        for row in scraped_data:
            # -1 because the ticket cost $1
            x = float(row[0].replace('$', "").replace(',', "")) - 1
            pX = 1.0 / float(row[1][5:])
            pXTotal += pX
            TotalExpectedValue += (x * pX)
        # Chance of losing
        TotalExpectedValue += (-1 * (1-pXTotal))
        print("$1 To play, GameID: "+gameID+". Game Expected Value:", TotalExpectedValue)
    else:
        print("Something went wrong! No data found for " + str(gameID))
    # Sanity delay
    # time.sleep(1)
