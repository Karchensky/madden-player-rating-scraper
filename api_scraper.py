import requests
import pandas as pd

# Define the API URL
url = "https://drop-api.ea.com/rating/madden-nfl"

# Send a GET request to the API
response = requests.get(url)

# Check for successful response
if response.status_code != 200:
    print(f"Error: Unable to fetch data (Status code: {response.status_code})")
    exit()

# Parse the JSON data
try:
    data = response.json()
except ValueError as e:
    print(f"Error parsing JSON: {e}")
    exit()

# Extract relevant player data
players = []
for player in data.get('items', []):
    # General player info with explicit None handling
    player_data = {
        'ID': player.get('id', None),
        'Overall Rating': player.get('overallRating', None),
        'First Name': player.get('firstName', None),
        'Last Name': player.get('lastName', None),
        'Birthdate': player.get('birthdate', None),
        'Height (inches)': player.get('height', None),
        'Weight (lbs)': player.get('weight', None),
        'College': player.get('college', None),
        'Handedness': player.get('handedness', None),
        'Age': player.get('age', None),
        'Jersey Number': player.get('jerseyNum', None),
        'Years Pro': player.get('yearsPro', None),
        'Team': player.get('team', {}).get('label') if player.get('team') else None,
        'Position': player.get('position', {}).get('label') if player.get('position') else None,
        'Iteration': player.get('iteration', {}).get('label') if player.get('iteration') else None,
        'Archetype': player.get('archetype', {}).get('label') if player.get('archetype') else None,
    }

    # Player stats
    stats = player.get('stats', {})
    for stat_name, stat_value in stats.items():
        if isinstance(stat_value, dict):
            player_data[stat_name] = stat_value.get('value', None)
        else:
            player_data[stat_name] = stat_value

    # Append player data to the list
    players.append(player_data)

# Create a DataFrame
df = pd.DataFrame(players)

# Export to CSV
output_file = "madden_players_data.csv"
df.to_csv(output_file, index=False)

print(f"Data successfully exported to {output_file}")