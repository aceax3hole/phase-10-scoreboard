import streamlit as st
import json

# Load phase list from JSON file
PHASES_FILE = "phases.json"
try:
    with open(PHASES_FILE, "r") as f:
        PHASES = json.load(f)
except Exception:
    PHASES = [
        "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5",
        "Phase 6", "Phase 7", "Phase 8", "Phase 9", "Phase 10"
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
    st.rerun()

# Function to update score
def update_score(player, score, completed):
    if player in st.session_state["game_state"]["players"]:
        st.session_state["game_state"]["total_scores"][player] += int(score)
        
        if completed:
            current_phase_index = PHASES.index(st.session_state["game_state"]["phases"][player])
            if current_phase_index < len(PHASES) - 1:
                st.session_state["game_state"]["phases"][player] = PHASES[current_phase_index + 1]
    st.rerun()

# Function to soft reset (keep players but reset scores)
def soft_reset():
    for player in st.session_state["game_state"]["players"]:
        st.session_state["game_state"]["total_scores"][player] = 0
        st.session_state["game_state"]["phases"][player] = PHASES[0]
    st.rerun()

# Function to full reset (clear all data)
def total_reset():
    st.session_state["game_state"] = {
        "players": [],
        "scores": {},
        "phases": {},
        "total_scores": {}
    }
    st.rerun()

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
        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])

        col1.write(f"**{player}**")
        col2.write(st.session_state["game_state"]["phases"][player])
        
        # Checkbox for phase completion
        phase_completed = col3.checkbox("✔", key=f"phase_{player}")
        
        # Score input
        score_input = col4.number_input(f"Score for {player}", min_value=0, key=f"score_{player}")
        
        if st.button(f"Update {player}"):
            update_score(player, score_input, phase_completed)
        
        # Display total score
        col5.write(f"Total: {st.session_state["game_state"]["total_scores"].get(player, 0)}")

# Buttons for resetting the game
st.button("Soft Reset", on_click=soft_reset)
st.button("Total Reset", on_click=total_reset)
