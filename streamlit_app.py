# Import necessary libraries
import streamlit as st
import pandas as pd

# Constants
POINTS_PER_HOLE = 27
DOLLAR_PER_POINT = 3

# Helper function to calculate dollars won
def calculate_dollars_won(points_won, dollar_per_point):
    return (points_won * dollar_per_point * 2) - ((9 - points_won) * dollar_per_point)

# Main function to run the app
def main():
    st.title("Golf Game App - 9's")
    
    # User input for number of players
    num_players = st.number_input("Enter number of players", min_value=1, value=3)
    
    # Create a dataframe to store points and dollars won
    columns = ['Hole', 'Points Allocated'] + [f'Player {i+1} Points' for i in range(num_players)] + [f'Player {i+1} Dollars' for i in range(num_players)]
    data = pd.DataFrame(columns=columns)
    
    # Fill the hole and points allocated columns
    data['Hole'] = range(1, 19)
    data['Points Allocated'] = 9
    
    # Input fields for points won
    for hole in range(1, 19):
        st.subheader(f'Hole {hole}')
        points_won = []
        for player in range(num_players):
            points = st.number_input(f'Player {player+1} Points Won (Hole {hole})', min_value=0, max_value=9, key=f'{hole}_{player}')
            points_won.append(points)
            data.loc[data['Hole'] == hole, f'Player {player+1} Points'] = points
        
        # Calculate dollars won for each player
        for player in range(num_players):
            points = points_won[player]
            dollars = calculate_dollars_won(points, DOLLAR_PER_POINT)
            data.loc[data['Hole'] == hole, f'Player {player+1} Dollars'] = dollars
    
    # Display the data
    st.subheader("Game Data")
    st.dataframe(data)
    
    # Summary of total points and dollars won
    st.subheader("Summary")
    summary_data = pd.DataFrame(columns=['Player', 'Total Points', 'Total Dollars'])
    for player in range(num_players):
        total_points = data[f'Player {player+1} Points'].sum()
        total_dollars = data[f'Player {player+1} Dollars'].sum()
        summary_data = summary_data.append({'Player': f'Player {player+1}', 'Total Points': total_points, 'Total Dollars': total_dollars}, ignore_index=True)
    
    st.dataframe(summary_data)

# Run the app
if __name__ == "__main__":
    main()

