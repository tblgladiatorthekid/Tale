
import streamlit as st
import json
from datetime import datetime
import os

DATA_FILE = "heartbreak_data.json"

st.set_page_config(page_title="Heartbreak Meter 💔", page_icon="💔", layout="centered")

# --- Load Data ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# --- Save Data ---
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- Compute Total Heartbreak ---
def get_total_heartbreak(data):
    return sum(entry["severity"] for entry in data)

# --- Get Leaderboard ---
def get_leaderboard(data):
    return sorted(data, key=lambda x: x["severity"], reverse=True)[:5]

# --- App UI ---
st.markdown(
    "<h1 style='text-align: center; color: grey;'>💔 Heartbreak Meter 💔</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align: center; font-family: sans-serif; color: #666;'>A melancholic tracker of the soul’s silent aches...</p>",
    unsafe_allow_html=True,
)

# Load or initialize data
heartbreaks = load_data()
total = get_total_heartbreak(heartbreaks)

# Show Pixelated Broken Heart
st.image("https://emojicdn.elk.sh/💔", width=100)

# Display current total
st.markdown(f"### Total Heartbreak: {total}/100")

# Input new heartbreak
with st.form("heartbreak_form"):
    person = st.text_input("Who broke your heart?")
    reason = st.text_input("Why? (e.g., ghosted, faded away...)")
    severity = st.slider("Severity (0–100)", 0, 100, 10)
    submitted = st.form_submit_button("Add Heartbreak 💔")

if submitted:
    if total >= 100:
        st.warning("You're already at max heartbreak. Be gentle with yourself.")
    else:
        heartbreaks.append({
            "person": person,
            "reason": reason,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        })
        save_data(heartbreaks)
        st.experimental_rerun()

# Show leaderboard
st.markdown("## 💔 Top 5 Most Intense Heartbreaks")
for i, entry in enumerate(get_leaderboard(heartbreaks), 1):
    st.markdown(f"**{i}. {entry['person']}** - {entry['severity']}/100 — _{entry['reason']}_")

# Allow edit/delete
st.markdown("## ✏️ Edit or Delete Entries")
for i, entry in enumerate(heartbreaks):
    with st.expander(f"{i+1}. {entry['person']} - {entry['severity']}/100"):
        new_person = st.text_input(f"Edit name for entry {i+1}", value=entry["person"], key=f"name_{i}")
        new_reason = st.text_input(f"Edit reason for entry {i+1}", value=entry["reason"], key=f"reason_{i}")
        new_severity = st.slider(f"Edit severity for entry {i+1}", 0, 100, entry["severity"], key=f"severity_{i}")
        if st.button("Save Changes", key=f"save_{i}"):
            heartbreaks[i] = {
                "person": new_person,
                "reason": new_reason,
                "severity": new_severity,
                "timestamp": entry["timestamp"]
            }
            save_data(heartbreaks)
            st.success("Updated.")
            st.experimental_rerun()
        if st.button("Delete Entry", key=f"delete_{i}"):
            heartbreaks.pop(i)
            save_data(heartbreaks)
            st.warning("Deleted.")
            st.experimental_rerun()

# Final Message
if total >= 100:
    st.markdown("---")
    st.markdown(
        "<p style='color: darkred; font-size: 18px; text-align: center;'>"
        "I'm so sorry. You deserve to be loved. But I'm telling you, you are loved. "
        "Even if you feel you're alone, don't let your light go out. You're still here, and you're brave for doing that."
        "</p>",
        unsafe_allow_html=True
    )
