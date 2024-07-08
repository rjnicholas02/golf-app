# Import necessary libraries
import streamlit as st
import pandas as pd

# Helper function to calculate dollars won
def calculate_dollars_won(points_won, dollar_per_point):
    return (points_won * dollar_per_point * 2) - ((9 - points_won) * dollar_per_point)

# Main function to run the app
def main():
    st.title("Golf Game App - 9's")

    # User input for number of players
    num_players = st.number_input("Enter number of players", min_value=1, value=3)
    
    # User input for player names
    player_names = []
    for i in range(num_players):
        player_name = st.text_input(f'Enter name for Player {i+1}', f'Player {i+1}')
        player_names.append(player_name)
    
    # User input for dollar per point
    dollar_per_point = st.selectbox("Select dollar amount per point", [1, 2, 3, 4, 5], index=2)

    # Create a dataframe to store points and dollars won
    columns = ['Hole', 'Points Allocated'] + [f'{name} Points' for name in player_names] + [f'{name} Dollars' for name in player_names]
    data = pd.DataFrame(columns=columns)

    # Initialize points won dictionary
    points_won = {name: [0] * 18 for name in player_names}

    # Fill the hole and points allocated columns
    data['Hole'] = range(1, 19)
    data['Points Allocated'] = 9

    # Input buttons for points won
    for hole in range(1, 19):
        st.subheader(f'Hole {hole}')
        for idx, player_name in enumerate(player_names):
            st.write(f"{player_name}:")
            cols = st.columns(5)
            for point in range(1, 6):
                if cols[point-1].button(f'{point}', key=f'{hole}_{player_name}_{point}'):
                    points_won[player_name][hole-1] = point
            st.write(f"Points: {points_won[player_name][hole-1]}")
            data.loc[data['Hole'] == hole, f'{player_name} Points'] = points_won[player_name][hole-1]
        
        # Calculate dollars won for each player
        for player_name in player_names:
            points = points_won[player_name][hole-1]
            dollars = calculate_dollars_won(points, dollar_per_point)
            data.loc[data['Hole'] == hole, f'{player_name} Dollars'] = dollars

    # Display the data
    st.subheader("Game Data")
    st.dataframe(data)

    # Summary of total points and dollars won
    st.subheader("Summary")
    summary_data = pd.DataFrame(columns=['Player', 'Total Points', 'Total Dollars'])
    for player_name in player_names:
        total_points = sum(points_won[player_name])
        total_dollars = data[f'{player_name} Dollars'].sum()
        summary_row = pd.DataFrame({'Player': [player_name], 'Total Points': [total_points], 'Total Dollars': [total_dollars]})
        summary_data = pd.concat([summary_data, summary_row], ignore_index=True)

    st.dataframe(summary_data)

# Run the app
if __name__ == "__main__":
    main()
