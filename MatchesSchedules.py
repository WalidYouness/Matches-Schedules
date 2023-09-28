import requests
import csv
from bs4 import BeautifulSoup
import os

# Function to fetch match details from the website
def get_match_details(date):

    page_url = f"https://www.yallakora.com/match-center/مركز-المباريات?date={date}"
    page = requests.get(page_url)

    if page.status_code != 200:
        print(f"Failed to fetch data for date: {date}")
        return

    source = page.content
    soup = BeautifulSoup(source, 'lxml')
    match_details = []

    # Find all match cards on the page
    match_cards = soup.find_all('div', {'class': 'matchCard'})

    # Extract information from each match card
    for match_card in match_cards:
        champion_name = match_card.find('h2').text.strip()
        matches = match_card.find_all('li')

        for match in matches:
            team_a = match.find('div', {'class': 'teamA'}).text.strip()
            team_b = match.find('div', {'class': 'teamB'}).text.strip()
            score_elements = match.find_all('span', {'class': 'score'})
            score = f"{score_elements[0].text.strip()} - {score_elements[1].text.strip()}"
            match_time = match.find('span', {'class': 'time'}).text.strip()


            match_details.append({
                "Champion Name": champion_name,
                "Team A": team_a,
                "Team B": team_b,
                "Match Time": match_time,
                "Score": score
            })

    return match_details

# Function to save match details to a CSV file
def save_to_csv(match_details, file_name):

    if not match_details:
        print("No match details to save.")
        return

    # Get the keys (column names) from the first match detail dictionary
    keys = match_details[0].keys()

    with open(file_name, "w", encoding='utf-8-sig', newline='') as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        # Write the match details to the file
        dict_writer.writerows(match_details)
        print(f"Data saved to {file_name} successfully.")

if __name__ == "__main__":
    # Get the date from the user
    date = input("Please write the date in the form DD/MM/YYYY: ")
    # Define the file name for the CSV file
    file_name = os.path.join(os.getcwd(), 'matches_details.csv')

    # Get match details and save them to the CSV file
    match_details = get_match_details(date)
    save_to_csv(match_details, file_name)
