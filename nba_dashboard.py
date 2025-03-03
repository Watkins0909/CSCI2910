import requests
import json
from datetime import datetime

# Replace this with your API Key
API_KEY = "d9a8d5d0-8624-44a7-b52c-b403117a9448"
BASE_URL = "https://api.balldontlie.io/v1"

# Headers for authentication
HEADERS = {
    "Authorization": API_KEY
}

def search_player(name):
    """Search for an NBA player by name and print details."""
    url = f"{BASE_URL}/players?search={name}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        players = data.get("data", [])

        if not players:
            print(f"No players found for '{name}'.")
            return None

        for idx, player in enumerate(players, 1):
            print(f"{idx}. {player['first_name']} {player['last_name']} | Team: {player['team']['full_name']} | Position: {player['position']}")
        return players
    else:
        print("Error retrieving player data.")
        return None

def list_teams():
    """List all NBA teams."""
    url = f"{BASE_URL}/teams"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        teams = data.get("data", [])

        print("\nNBA Teams:")
        for team in teams:
            print(f"{team['id']}: {team['full_name']} ({team['abbreviation']}) - {team['conference']} Conference")
    else:
        print("Error retrieving teams.")

def get_team_games(team_id):
    """Get the most recent games for a specific NBA team, sorted by date (newest first)."""
    url = f"{BASE_URL}/games?team_ids[]={team_id}&per_page=10"  # Get more games for better sorting
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        games = data.get("data", [])

        if not games:
            print("No recent games found for this team.")
            return

        # Sorting the games by date (newest first)
        sorted_games = sorted(games, key=lambda g: datetime.fromisoformat(g['date'].rstrip("Z")), reverse=True)

        print("\nLeast Recent Games:")
        for game in sorted_games[:5]:  # Show only the latest 5 games
            home_team = game['home_team']['full_name']
            visitor_team = game['visitor_team']['full_name']
            home_score = game['home_team_score']
            visitor_score = game['visitor_team_score']
            game_date = game['date'][:10]  # Extract only the YYYY-MM-DD part
            
            print(f"Date: {game_date}")
            print(f"{home_team} vs {visitor_team}")
            print(f"Final Score: {home_score} - {visitor_score}\n")
    else:
        print("Error retrieving games.")

def create_and_save_starting_five():
    """
    Allow the user to create a starting five by searching for players.
    The selected five players are then saved to a JSON file.
    """
    starting_five = []
    print("\n=== Create Your Starting Five ===")
    while len(starting_five) < 5:
        print(f"\nSelect player {len(starting_five) + 1} for your starting five:")
        name = input("Enter player's name: ")
        players = search_player(name)
        if not players:
            continue

        try:
            choice = int(input("Select a player by number (or 0 to cancel): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 0:
            print("Cancelling selection. Please try again.")
            continue

        if 1 <= choice <= len(players):
            selected_player = players[choice - 1]
            # Check if the player is already in the starting five
            if any(p['id'] == selected_player['id'] for p in starting_five):
                print("Player already selected. Choose another player.")
                continue
            starting_five.append(selected_player)
            print(f"Added {selected_player['first_name']} {selected_player['last_name']} to your starting five.")
        else:
            print("Invalid selection. Try again.")

    # Display the created starting five
    print("\nYour Starting Five:")
    for player in starting_five:
        print(f"{player['first_name']} {player['last_name']} | Team: {player['team']['full_name']} | Position: {player['position']}")

    save_choice = input("Do you want to save this starting five? (y/n): ")
    if save_choice.lower() == "y":
        try:
            with open("starting_five.json", "w") as file:
                json.dump(starting_five, file, indent=4)
            print("Starting five saved to starting_five.json.")
        except Exception as e:
            print("Error saving file:", e)
    else:
        print("Starting five not saved.")

def display_starting_five():
    """Load and display the saved starting five from the JSON file."""
    try:
        with open("starting_five.json", "r") as file:
            starting_five = json.load(file)
        if not starting_five:
            print("No starting five found in the file.")
            return
        print("\n=== Saved Starting Five ===")
        for idx, player in enumerate(starting_five, 1):
            print(f"{idx}. {player['first_name']} {player['last_name']} | Team: {player['team']['full_name']} | Position: {player['position']}")
    except FileNotFoundError:
        print("No starting five has been saved yet.")
    except Exception as e:
        print("Error reading file:", e)

def main():
    """Main program loop."""
    while True:
        print("\n=== NBA Stats Dashboard ===")
        print("1. Search for a Player")
        print("2. List all Teams")
        print("3. Get oldest Games for a Team")
        print("4. Create and Save Starting Five")
        print("5. Display Saved Starting Five")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            name = input("Enter player's name to search: ")
            search_player(name)
        elif choice == "2":
            list_teams()
        elif choice == "3":
            team_id = input("Enter team ID: ")
            get_team_games(team_id)
        elif choice == "4":
            create_and_save_starting_five()
        elif choice == "5":
            display_starting_five()
        elif choice == "6":
            print("Exiting program...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
