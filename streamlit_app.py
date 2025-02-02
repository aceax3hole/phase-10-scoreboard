import streamlit as st
import json

# Load phase list (you can move this to an external JSON file)
PHASES = [
    "2 sets of 3", "1 set of 3 + 1 run of 4", "1 set of 4 + 1 run of 4", "1 run of 7", "1 run of 8",
    "1 run of 9", "2 sets of 4", "7 cards of one color", "1 set of 5 + 1 set of 2", "1 set of 5 + 1 set of 3",
    "1 run of 4 of one color", "1 run of 6 of one color", "1 run of 4 + 6 cards of one color", "1 run of 6 + 4 cards of one color", "8 cards of one color",
    "9 cards of one color", "3 sets of 3", "1 set of 4 + 1 run of 6", "1 set of 5 + 1 run of 5", "1 set of 5 + 5 cards of one color",
    "5 sets of 2", "1 run of 10", "10 cards of one color", "1 run of 5 of odd numbers of one color + 1 run of 5 of even numbers of one color", "1 set of 5 + 1 run of 5 odd numbers",
    "1 set of 5 + 1 run of 5 even numbers", "1 set of 4 + 1 run of 3 + 1 set of 3 of one color", "1 run of 5 + 1 run of 5 odd numbers of one color", "1 run of 5 + 1 run of 5 even numbers of one color", "2 sets of 5"

]

# Initialize game state in Streamlit session
if "game_state" not in st.session_state:
    st.session_state["game_state"] = {
        "players": [],
        "scores": {},
        "phases": {},
        "total_scores": {}
    }

# Function to add a player
def add_player(player_name):
    if player_name and player_name not in st.session_state["game_state"]["players"]:
        st.session_state["game_state"]["players"].append(player_name)
        st.session_state["game_state"]["phases"][player_name] = PHASES[0]  # Start at Phase 1
        st.session_state["game_state"]["scores"][player_name] = 0
        st.session_state["game_state"]["total_scores"][player_name] = 0
    st.experimental_rerun()

# Function to update score
def update_score(player, score, completed):
    if player in st.session_state["game_state"]["players"]:
        st.session_state["game_state"]["total_scores"][player] += int(score)
        
        if completed:
            current_phase_index = PHASES.index(st.session_state["game_state"]["phases"][player])
            if current_phase_index < len(PHASES) - 1:
                st.session_state["game_state"]["phases"][player] = PHASES[current_phase_index + 1]
    st.experimental_rerun()

# Function to soft reset (keep players but reset scores)
def soft_reset():
    for player in st.session_state["game_state"]["players"]:
        st.session_state["game_state"]["total_scores"][player] = 0
        st.session_state["game_state"]["phases"][player] = PHASES[0]
    st.experimental_rerun()

# Function to full reset (clear all data)
def total_reset():
    st.session_state["game_state"] = {
        "players": [],
        "scores": {},
        "phases": {},
        "total_scores": {}
    }
    st.experimental_rerun()

# UI Layout
st.title("Phase Out Scoreboard")

# Add Player Section
player_name = st.text_input("Enter Player Name")
if st.button("Add Player"):
    add_player(player_name)

# Display Scoreboard
st.subheader("Current Scores & Phases")
if st.session_state["game_state"]["players"]:
    for player in st.session_state["game_state"]["players"]:
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

        col1.write(f"**{player}**")
        col2.write(st.session_state["game_state"]["phases"][player])
        
        # Checkbox for phase completion
        phase_completed = col3.checkbox("✔", key=f"phase_{player}")
        
        # Score input
        score_input = col4.number_input(f"Score for {player}", min_value=0, key=f"score_{player}")
        
        if st.button(f"Update {player}"):
            update_score(player, score_input, phase_completed)

# Buttons for resetting the game
st.button("Soft Reset", on_click=soft_reset)
st.button("Total Reset", on_click=total_reset)
