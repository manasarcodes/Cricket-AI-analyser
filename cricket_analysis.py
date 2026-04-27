import pandas as pd
import json

# --- CONFIGURATION ---
# Change 'your_match_file.json' to the actual name of your file
JSON_FILE = r'F:\manasa-backup_21-07-2025\Projects\Cricket ai analyser\1527584.json'

# --- THE CODE ---
try:
    # 1. Load the data
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)

    # 2. Extract data into a list
    delivery_list = []
    for inning in data['innings']:
        team = inning['team']
        for over_data in inning['overs']:
            over_num = over_data['over']
            for delivery in over_data['deliveries']:
                delivery_list.append({
                    'team': team,
                    'over': over_num,
                    'batter': delivery['batter'],
                    'bowler': delivery['bowler'],
                    'runs': delivery['runs']['total']
                })

    # 3. Create the table
    df = pd.DataFrame(delivery_list)

    # 4. Show the result
    print("Data loaded successfully! Here is the first 5 rows:")
    print(df.head())

except Exception as e:
    print(f"An error occurred: {e}")