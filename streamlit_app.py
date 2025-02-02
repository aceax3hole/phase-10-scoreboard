import streamlit as st
import json

# Load phase list from JSON file
PHASES_FILE = "phases.json"
try:
    with open(PHASES_FILE, "r") as f:
        PHASES = json.load(f)
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
        "selected_phases": PHASES[:3] if PHASES else ["Unknown Phase"]
    }

# Function to add a player
def add_player(player_name):
    if player_name and player_name not in st.session_state["game_state"]["players"]:
        st.session_state["game_state"]["players"].append(player_name)
        st.session_state["game_state"]["phases"][player_name] = st.session_state["game_state"].get("selected_phases", PHASES)[0]
        st.session_state["game_state"]["scores"][player_name] = 0
        st.session_state["game_state"]["total_scores"][player_name] = 0
    st.rerun()

# Function to update all players
def update_all_players():
    for player in st.session_state["game_state"]["players"]:
        update_score(player, st.session_state["game_state"]["scores"].get(player, 0), st.session_state["game_state"]["phases"].get(player, False))
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
        
        # Reset checkbox state
        st.session_state["game_state"]["phases"][player] = False
    st.rerun()

# Function to soft reset (keep players but reset scores)
def soft_reset():
    for player in st.session_state["game_state"]["players"]:
        st.session_state["game_state"]["total_scores"][player] = 0
        st.session_state["game_state"]["phases"][player] = st.session_state["game_state"].get("selected_phases", PHASES)[0]
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

# Sidebar for Phase Selection
st.sidebar.header("Select Phases to Use")
if "selected_phases" not in st.session_state["game_state"]:
    st.session_state["game_state"]["selected_phases"] = PHASES[:3] if PHASES else ["Unknown Phase"]

selected_phases = st.sidebar.multiselect("Choose Phases", PHASES, default=st.session_state["game_state"]["selected_phases"])
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

# Display Scoreboard with Streamlit Elements
st.subheader("Current Scores & Phases")
num_players = len(st.session_state["game_state"]["players"])
num_cols = max(2, (num_players + 1) // 2)
cols = st.columns(num_cols)

for i, player in enumerate(st.session_state["game_state"]["players"]):
    with cols[i % num_cols]:
        st.markdown(f"**{player}**")
        st.write(f"Current Phase: {st.session_state["game_state"]["phases"].get(player, PHASES[0])}")
        st.write(f"Total Score: {st.session_state["game_state"]["total_scores"].get(player, 0)}")
        
        # Checkbox for phase completion
        completed = st.checkbox("Phase Complete", key=f"phase_{player}")
        
        # Score input
        score_input = st.number_input(f"Score for {player}", min_value=0, key=f"score_{player}")
        
        # Update Button
        if st.button(f"Update {player}"):
            update_score(player, score_input, completed)

# Buttons for resetting and updating
st.button("Soft Reset", on_click=soft_reset)
st.button("Total Reset", on_click=total_reset)
st.button("Update All Players", on_click=update_all_players)
