import streamlit as st
import json

# Load phase list from JSON file
PHASES_FILE = "phases.json"
try:
    with open(PHASES_FILE, "r") as f:
        PHASES = json.load(f)
    if not isinstance(PHASES, list) or not PHASES:  # Ensure it's a valid list
        raise ValueError("Phase list is empty or invalid")
except Exception as e:
    st.error(f"Error loading phases.json: {e}")
    PHASES = ["Unknown Phase"]

# Initialize game state in Streamlit session
if "game_state" not in st.session_state:
    st.session_state["game_state"] = {
        "players": [],
        "scores": {},
        "phases": {},
        "total_scores": {},
        "selected_phases": PHASES[:3] if PHASES else ["Unknown Phase"]  # Ensure valid default phases
    }

# Function to add a player
def add_player(player_name):
    if player_name and player_name not in st.session_state["game_state"]["players"]:
        st.session_state["game_state"]["players"].append(player_name)
        st.session_state["game_state"]["phases"][player_name] = st.session_state["game_state"].get("selected_phases", PHASES)[0]
        st.session_state["game_state"]["scores"][player_name] = 0
        st.session_state["game_state"]["total_scores"][player_name] = 0
    st.rerun()

# Function to update score
def update_score(player, score, completed):
    if player in st.session_state["game_state"]["players"]:
        st.session_state["game_state"]["total_scores"][player] += int(score)
        
        if completed:
            selected_phases = st.session_state["game_state"].get("selected_phases", PHASES)
            current_phase_index = selected_phases.index(
                st.session_state["game_state"]["phases"].get(player, selected_phases[0])
            ) if selected_phases else -1
            if current_phase_index != -1 and current_phase_index < len(selected_phases) - 1:
                st.session_state["game_state"]["phases"][player] = selected_phases[current_phase_index + 1]
    st.rerun()

# Function to soft reset (keep players but reset scores)
def soft_reset():
    selected_phases = st.session_state["game_state"].get("selected_phases", PHASES)
    for player in st.session_state["game_state"]["players"]:
        st.session_state["game_state"]["total_scores"][player] = 0
        st.session_state["game_state"]["phases"][player] = selected_phases[0]
    st.rerun()

# Function to full reset (clear all data)
def total_reset():
    st.session_state["game_state"] = {
        "players": [],
        "scores": {},
        "phases": {},
        "total_scores": {},
        "selected_phases": PHASES[:3] if PHASES else ["Unknown Phase"]
    }
    st.rerun()

# UI Layout
st.title("Phase Out Scoreboard")

# Phase Selection Section
st.subheader("Select Phases to Use")
if "selected_phases" not in st.session_state["game_state"]:
    st.session_state["game_state"]["selected_phases"] = PHASES[:3] if PHASES else ["Unknown Phase"]

selected_phases = st.multiselect("Choose Phases", PHASES, default=st.session_state["game_state"]["selected_phases"])
if selected_phases:
    st.session_state["game_state"]["selected_phases"] = selected_phases
    for player in st.session_state["game_state"]["players"]:
        st.session_state["game_state"]["phases"][player] = selected_phases[0]  # Reset player phase to first selected
    st.rerun()

# Add Player Section
st.subheader("Add a Player")
player_name = st.text_input("Enter Player Name")
if st.button("Add Player"):
    add_player(player_name)

# Display Scoreboard
st.subheader("Current Scores & Phases")
if st.session_state["game_state"]["players"]:
    for player in st.session_state["game_state"]["players"]:
        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])

        col1.write(f"**{player}**")
        col2.write(st.session_state["game_state"]["phases"].get(player, st.session_state["game_state"].get("selected_phases", PHASES)[0]))
        
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
