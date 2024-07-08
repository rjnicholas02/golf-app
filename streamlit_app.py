# Import necessary libraries
import streamlit as st
import pandas as pd

# Helper function to calculate dollars won
def calculate_dollars_won(points_won, dollar_per_point):
    return (points_won * dollar_per_point * 2) - ((9 - points_won) * dollar_per_point)

# Main function to run the app
def main():
    st.title("Golf Game App - 9's")

    # User input for player names
    player_names = [st.text_input(f'Enter name for Player {i+1}', f'Player {i+1}') for i in range(3)]
    
    # User input for dollar per point
    dollar_per_point = st.selectbox("Select dollar amount per point", [1, 2, 3, 4, 5], index=2)

    # Initialize session state to track current hole and scores
    if 'current_hole' not in st.session_state:
        st.session_state.current_hole = 1
    if 'points_won' not in st.session_state:
        st.session_state.points_won = {name: [0] * 18 for name in player_names}
    if 'data' not in st.session_state:
        columns = ['Hole', 'Points Allocated'] + [f'{name} Points' for name in player_names] + [f'{name} Dollars' for name in player_names]
        st.session_state.data = pd.DataFrame(columns=columns)
        st.session_state.data['Hole'] = range(1, 19)
        st.session_state.data['Points Allocated'] = 9

    # Current hole
    hole = st.session_state.current_hole
    st.subheader(f'Hole {hole}')

    # Input buttons for points won
    for idx, player_name in enumerate(player_names):
        st.write(f"{player_name}:")
        cols = st.columns(5)
        for point in range(1, 6):
            if cols[point-1].button(f'{point}', key=f'{hole}_{player_name}_{point}'):
                st.session_state.points_won[player_name][hole-1] = point
        st.write(f"Points: {st.session_state.points_won[player_name][hole-1]}")

    # Enter button to submit the scores and move to the next hole
    if st.button('Enter'):
        for player_name in player_names:
            points = st.session_state.points_won[player_name][hole-1]
            st.session_state.data.loc[st.session_state.data['Hole'] == hole, f'{player_name} Points'] = points
            dollars = calculate_dollars_won(points, dollar_per_point)
            st.session_state.data.loc[st.session_state.data['Hole'] == hole, f'{player_name} Dollars'] = dollars
        
        if hole < 18:
            st.session_state.current_hole += 1
        else:
            st.subheader("Game Completed")

    # Display the summary
    st.subheader("Summary")
    summary_data = pd.DataFrame(columns=['Player', 'Total Points', 'Total Dollars'])
    for player_name in player_names:
        total_points = sum(st.session_state.points_won[player_name])
        total_dollars = st.session_state.data[f'{player_name} Dollars'].sum()
        summary_row = pd.DataFrame({'Player': [player_name], 'Total Points': [total_points], 'Total Dollars': [total_dollars]})
        summary_data = pd.concat([summary_data, summary_row], ignore_index=True)

    st.dataframe(summary_data)

    # Edit table
    st.subheader("Edit Scores")
    edited_data = st.session_state.data.copy()

    # Edit scores directly in the table
    for idx, player_name in enumerate(player_names):
        for hole in range(1, 19):
            points_col = f'{player_name} Points'
            new_points = st.number_input(f'{player_name} Points (Hole {hole})', min_value=0, max_value=5, value=int(edited_data.loc[edited_data['Hole'] == hole, points_col].values[0]), key=f'{hole}_{player_name}_edit')
            edited_data.loc[edited_data['Hole'] == hole, points_col] = new_points
            dollars_col = f'{player_name} Dollars'
            edited_data.loc[edited_data['Hole'] == hole, dollars_col] = calculate_dollars_won(new_points, dollar_per_point)

    if st.button('Save Changes'):
        st.session_state.data = edited_data.copy()
        st.success("Changes saved successfully")

    st.dataframe(edited_data)

# Run the app
if __name__ == "__main__":
    main()
