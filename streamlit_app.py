import streamlit as st
import json
import os
import pandas as pd
import copy

# Load phases from JSON file
with open("phases.json", "r") as file:
    phases = json.load(file)

# Initialize session state for dynamic elements
if "players" not in st.session_state:
    st.session_state.players = []
if "scores" not in st.session_state:
    st.session_state.scores = {}
if "phase_progress" not in st.session_state:
    st.session_state.phase_progress = {}
if "game_history" not in st.session_state:
    st.session_state.game_history = []
if "selected_phases" not in st.session_state:
    st.session_state.selected_phases = phases

# Header and layout
st.title("Phase 10 Scoreboard")
st.sidebar.header("Game Settings")

# Player Management
st.sidebar.subheader("Add Players")
new_player = st.sidebar.text_input("Player Name")
if st.sidebar.button("Add Player") and new_player:
    if new_player not in st.session_state.players:
        st.session_state.players.append(new_player)
        st.session_state.scores[new_player] = 0
        st.session_state.phase_progress[new_player] = 0

# Display players and allow removal
if st.session_state.players:
    st.sidebar.subheader("Current Players")
    for player in st.session_state.players:
        if st.sidebar.button(f"Remove {player}"):
            st.session_state.players.remove(player)
            del st.session_state.scores[player]
            del st.session_state.phase_progress[player]

# Phase Selection
st.sidebar.subheader("Select Phases")
selected_phases = st.sidebar.multiselect("Choose which phases to include:", options=phases, default=phases)
st.session_state.selected_phases = selected_phases

# New Game Button
if st.sidebar.button("New Game"):
    st.session_state.scores = {player: 0 for player in st.session_state.players}
    st.session_state.phase_progress = {player: 0 for player in st.session_state.players}
    st.session_state.game_history = []
    st.success("Game reset successfully!")

# Main interface
if st.session_state.players:
    st.subheader("Leaderboard")
    leaderboard_data = {
        "Player": st.session_state.players,
        "Score": [st.session_state.scores[player] for player in st.session_state.players],
        "Phase": [st.session_state.selected_phases[st.session_state.phase_progress[player]] if st.session_state.phase_progress[player] < len(st.session_state.selected_phases) else "Completed" for player in st.session_state.players],
    }
    leaderboard_df = pd.DataFrame(leaderboard_data).sort_values(by="Score", ascending=False)
    st.table(leaderboard_df)

    st.subheader("Score Entry")
    for player in st.session_state.players:
        with st.expander(f"Enter Score for {player}"):
            new_score = st.number_input(f"Score for {player}", min_value=0, step=5, key=f"score_{player}")
            phase_complete = st.checkbox(f"Phase Complete for {player}", key=f"phase_{player}")
            if st.button(f"Update {player}"):
                st.session_state.scores[player] -= new_score
                if phase_complete:
                    st.session_state.phase_progress[player] += 1

    # Save game state
    if st.button("Save Game State"):
        game_state = {
            "players": copy.deepcopy(st.session_state.players),
            "scores": copy.deepcopy(st.session_state.scores),
            "phase_progress": copy.deepcopy(st.session_state.phase_progress),
            "selected_phases": copy.deepcopy(st.session_state.selected_phases)
        }
        st.session_state.game_history.append(game_state)
        st.success("Game state saved!")

    # Export game history
    if st.button("Export Game History"):
        if st.session_state.game_history:
            flattened_history = []
            for state in st.session_state.game_history:
                for player in state["players"]:
                    flattened_history.append({
                        "Player": player,
                        "Score": state["scores"][player],
                        "Phase": state["selected_phases"][state["phase_progress"][player]] if state["phase_progress"][player] < len(state["selected_phases"]) else "Completed"
                    })
            history_df = pd.DataFrame(flattened_history)
            history_csv = history_df.to_csv(index=False).encode("utf-8")
            st.download_button("Download Game History as CSV", data=history_csv, file_name="game_history.csv", mime="text/csv")
        else:
            st.warning("No game history available to export.")
else:
    st.write("Add players to begin the game.")

# Footer
st.sidebar.write("\n---\n")
st.sidebar.write("Developed for Phase 10 enthusiasts.")
