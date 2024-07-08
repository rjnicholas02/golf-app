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
        columns = ['Hole'] + [f'{name} Points' for name in player_names] + [f'{name} Dollars' for name in player_names]
        st.session_state.data = pd.DataFrame(columns=columns)
        st.session_state.data['Hole'] = range(1, 19)
    if 'confirm_reset' not in st.session_state:
        st.session_state.confirm_reset = False

    # Function to set the current hole
    def set_hole(hole):
        st.session_state.current_hole = hole

    # Display hole buttons for navigation
    st.subheader("Select Hole to Edit")
    cols = st.columns(6)
    for hole in range(1, 19):
        col = cols[(hole-1) % 6]
        if col.button(f'Hole {hole}', key=f'select_hole_{hole}'):
            set_hole(hole)

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
                st.session_state.data.loc[st.session_state.data['Hole'] == hole, f'{player_name} Points'] = point
                st.session_state.data.loc[st.session_state.data['Hole'] == hole, f'{player_name} Dollars'] = calculate_dollars_won(point, dollar_per_point)
        st.write(f"Points: {st.session_state.points_won[player_name][hole-1]}")

    # Display the summary
    st.subheader("Summary")
    summary_data = pd.DataFrame(columns=['Player', 'Total Points'])
    for player_name in player_names:
        total_points = sum(st.session_state.points_won[player_name])
        summary_row = pd.DataFrame({'Player': [player_name], 'Total Points': [total_points]})
        summary_data = pd.concat([summary_data, summary_row], ignore_index=True)

    st.dataframe(summary_data)

    # Display hole-by-hole summary
    st.subheader("Hole-by-Hole Summary")
    hole_summary_data = st.session_state.data.copy()
    st.dataframe(hole_summary_data)

    # Button to reset the game
    if st.button('Start Over'):
        st.session_state.confirm_reset = True

    if st.session_state.confirm_reset:
        if st.button('Confirm Reset'):
            st.session_state.current_hole = 1
            st.session_state.points_won = {name: [0] * 18 for name in player_names}
            st.session_state.data = pd.DataFrame(columns=['Hole'] + [f'{name} Points' for name in player_names] + [f'{name} Dollars' for name in player_names])
            st.session_state.data['Hole'] = range(1, 19)
            st.session_state.confirm_reset = False
            st.experimental_rerun()
        if st.button('Cancel'):
            st.session_state.confirm_reset = False

if __name__ == "__main__":
    main()
