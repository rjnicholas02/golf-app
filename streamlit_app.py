# Import necessary libraries
import streamlit as st
import pandas as pd

# Constants
POINTS_PER_HOLE = 27
DOLLAR_PER_POINT = 3
MAX_POINTS = 9

# Helper function to calculate dollars won
def calculate_dollars_won(points_won, dollar_per_point):
    return (points_won * dollar_per_point * 2) - ((MAX_POINTS - points_won) * dollar_per_point)

# Main function to run the app
def main():
    st.title("Golf Game App - 9's")

    # User input for number of players
    num_players = st.number_input("Enter number of players", min_value=1, value=3)

    # Create a dataframe to store points and dollars won
    columns = ['Hole', 'Points Allocated'] + [f'Player {i+1} Points' for i in range(num_players)] + [f'Player {i+1} Dollars' for i in range(num_players)]
    data = pd.DataFrame(columns=columns)

    # Initialize points won dictionary
    points_won = {f'Player {i+1}': [0] * 18 for i in range(num_players)}

    # Fill the hole and points allocated columns
    data['Hole'] = range(1, 19)
    data['Points Allocated'] = 9

    # Input buttons for points won
    for hole in range(1, 19):
        st.subheader(f'Hole {hole}')
        for player in range(num_players):
            player_key = f'Player {player+1}'
            if st.button(f'{player_key} +1 (Hole {hole})', key=f'{hole}_{player}_plus'):
                if points_won[player_key][hole-1] < MAX_POINTS:
                    points_won[player_key][hole-1] += 1
            if st.button(f'{player_key} -1 (Hole {hole})', key=f'{hole}_{player}_minus'):
                if points_won[player_key][hole-1] > 0:
                    points_won[player_key][hole-1] -= 1
            data.loc[data['Hole'] == hole, f'{player_key} Points'] = points_won[player_key][hole-1]
        
        # Calculate dollars won for each player
        for player in range(num_players):
            player_key = f'Player {player+1}'
            points = points_won[player_key][hole-1]
            dollars = calculate_dollars_won(points, DOLLAR_PER_POINT)
            data.loc[data['Hole'] == hole, f'{player_key} Dollars'] = dollars

    # Display the data
    st.subheader("Game Data")
    st.dataframe(data)

    # Summary of total points and dollars won
    st.subheader("Summary")
    summary_data = pd.DataFrame(columns=['Player', 'Total Points', 'Total Dollars'])
    for player in range(num_players):
        player_key = f'Player {player+1}'
        total_points = sum(points_won[player_key])
        total_dollars = data[f'{player_key} Dollars'].sum()
        summary_row = pd.DataFrame({'Player': [player_key], 'Total Points': [total_points], 'Total Dollars': [total_dollars]})
        summary_data = pd.concat([summary_data, summary_row], ignore_index=True)

    st.dataframe(summary_data)

# Run the app
if __name__ == "__main__":
    main()
