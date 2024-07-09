# Import necessary libraries
import streamlit as st
import pandas as pd

# Helper function to calculate dollars won
def calculate_dollars_won(points_won, dollar_per_point):
    return (points_won * dollar_per_point * 2) - ((9 - points_won) * dollar_per_point)

# Main function to run the app
def main():
    # Set the title and description of the app
    st.set_page_config(page_title="Golf Game Tracker - 9's", page_icon="⛳", layout="centered")
    st.title("Golf Game Tracker - 9's")
    st.write("Track your golf game scores and winnings with ease!")

    # Initialize player names in session state
    if 'player_names' not in st.session_state:
        st.session_state.player_names = [f'Player {i+1}' for i in range(3)]
    
    # Display user input for player names with header and color
    st.markdown("## Player Names")
    player_names = []
    for i in range(3):
        player_name = st.text_input(f'Enter name for Player {i+1}', st.session_state.player_names[i])
        player_names.append(player_name)
    
    # Update player names in session state
    st.session_state.player_names = player_names

    # User input for dollar per point
    st.markdown("## Dollar Amount per Point")
    dollar_per_point = st.selectbox("Select dollar amount per point", [1, 2, 3, 4, 5], index=2)

    # Initialize session state to track current hole and scores
    if 'current_hole' not in st.session_state:
        st.session_state.current_hole = 1
    if 'points_won' not in st.session_state or set(st.session_state.points_won.keys()) != set(player_names):
        st.session_state.points_won = {name: [0] * 18 for name in player_names}
    if 'data' not in st.session_state or set(st.session_state.data.columns) != set(['Hole'] + [f'{name} Points' for name in player_names]):
        columns = ['Hole'] + [f'{name} Points' for name in player_names]
        st.session_state.data = pd.DataFrame(columns=columns)
        st.session_state.data['Hole'] = range(1, 19)
    if 'confirm_reset' not in st.session_state:
        st.session_state.confirm_reset = False

    # Ensure player points_won and data columns are up-to-date
    new_columns = ['Hole'] + [f'{name} Points' for name in player_names]
    st.session_state.data = st.session_state.data.reindex(columns=new_columns)
    
    # Function to set the current hole
    def set_hole(hole):
        st.session_state.current_hole = hole

    # Add CSS for horizontal scrolling and responsive design
    st.markdown(
        """
        <style>
        .hole-buttons-container {
            display: flex;
            flex-wrap: nowrap;
            overflow-x: auto;
            padding: 10px 0;
            margin-bottom: 20px;
        }
        .hole-button {
            flex: 0 0 auto;
            margin-right: 10px;
        }
        .point-button-container {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        .point-button {
            flex: 1;
            margin: 0 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display hole buttons for navigation with horizontal scrolling
    st.markdown("## Select Hole to Edit")
    st.markdown('<div class="hole-buttons-container">', unsafe_allow_html=True)
    for hole in range(1, 19):
        st.markdown(f'<button class="hole-button" onclick="window.location.href=\'#Hole{hole}\'">{hole}</button>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Current hole
    hole = st.session_state.current_hole
    st.markdown(f'<h3 id="Hole{hole}">Hole {hole}</h3>', unsafe_allow_html=True)

    # Input buttons for points won with horizontal layout
    for idx, player_name in enumerate(player_names):
        st.markdown(f"#### {player_name}:")
        st.markdown('<div class="point-button-container">', unsafe_allow_html=True)
        for point in range(1, 6):
            if st.button(f'{point}', key=f'{hole}_{player_name}_{point}', help=f"Assign {point} points to {player_name} for Hole {hole}"):
                st.session_state.points_won[player_name][hole-1] = point
                st.session_state.data.loc[st.session_state.data['Hole'] == hole, f'{player_name} Points'] = point
        st.markdown('</div>', unsafe_allow_html=True)
        st.write(f"Points: {st.session_state.points_won[player_name][hole-1]}")

    # Display the summary with color and style
    st.markdown("## Summary")
    summary_data = pd.DataFrame(columns=['Player', 'Total Points', 'Total Dollars'])
    for player_name in player_names:
        total_points = sum(st.session_state.points_won[player_name])
        total_dollars = sum(calculate_dollars_won(p, dollar_per_point) for p in st.session_state.points_won[player_name] if p > 0)
        summary_row = pd.DataFrame({'Player': [player_name], 'Total Points': [total_points], 'Total Dollars': [total_dollars]})
        summary_data = pd.concat([summary_data, summary_row], ignore_index=True)

    st.dataframe(summary_data.style.format({'Total Dollars': '${:,.2f}'}).set_properties(**{'text-align': 'center'}))

    # Display hole-by-hole summary with color and style
    st.markdown("## Hole-by-Hole Summary")
    hole_summary_data = st.session_state.data[['Hole'] + [f'{name} Points' for name in player_names]].copy()
    st.dataframe(hole_summary_data.style.set_properties(**{'text-align': 'center'}))

    # Button to reset the game with color and confirmation dialog
    if st.button('Start Over', help="Click to start a new game"):
        st.session_state.confirm_reset = True

    if st.session_state.confirm_reset:
        if st.button('Confirm Reset', help="Confirm to reset all data and start over"):
            st.session_state.current_hole = 1
            st.session_state.points_won = {name: [0] * 18 for name in player_names}
            st.session_state.data = pd.DataFrame(columns=['Hole'] + [f'{name} Points' for name in player_names])
            st.session_state.data['Hole'] = range(1, 19)
            st.session_state.confirm_reset = False
            st.experimental_rerun()
        if st.button('Cancel', help="Cancel reset and continue game"):
            st.session_state.confirm_reset = False

if __name__ == "__main__":
    main()
