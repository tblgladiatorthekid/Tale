
import streamlit as st
import json
from datetime import datetime
import os

DATA_FILE = "heartbreak_data.json"

st.set_page_config(page_title="Heartbreak Meter 💔",
                   page_icon="💔",
                   layout="centered")


# --- Load Data ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Corrupted or empty file
            return []
    return []


# --- Save Data ---
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


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
    "<p style='text-align: center; font-family: sans-serif; color: #666;'>"
    "A melancholic tracker of the soul’s silent aches..."
    "</p>",
    unsafe_allow_html=True,
)


# Load existing entries and compute total
heartbreaks = load_data()
total = get_total_heartbreak(heartbreaks)

st.image("https://emojicdn.elk.sh/💔", width=100)
st.markdown(f"### Total Heartbreak: {total}/100")


# --- Input New Heartbreak ---
with st.form("heartbreak_form"):
    person = st.text_input("Who broke your heart?")
    reason = st.text_input("Why? (e.g., ghosted, faded away...)")
    severity = st.slider("Severity (0–100)", 0, 100, 10)
    submitted = st.form_submit_button("Add Heartbreak 💔")

if submitted:
    # Validate non-empty fields
    if not person.strip() or not reason.strip():
        st.error("Please fill in both 'Who' and 'Why' fields before submitting.")
    else:
        new_total = total + severity
        # Prevent exceeding 100
        if new_total > 100:
            st.warning("That would push you past 100 — try a smaller number of heartbreak points.")
        else:
            entry = {
                "person": person.strip(),
                "reason": reason.strip(),
                "severity": severity,
                "timestamp": datetime.now().isoformat()
            }
            heartbreaks.append(entry)
            save_data(heartbreaks)
            st.experimental_rerun()


# --- Leaderboard ---
st.markdown("## 💔 Top 5 Most Intense Heartbreaks")
for i, entry in enumerate(get_leaderboard(heartbreaks), start=1):
    st.markdown(f"**{i}. {entry['person']}** - {entry['severity']}/100 — _{entry['reason']}_")

# --- Edit or Delete Entries ---
st.markdown("## ✏️ Edit or Delete Entries")

for entry in heartbreaks:
    ts = entry["timestamp"]
    label = f"{entry['person']} — {entry['severity']}/100"
    with st.expander(label):
        new_person = st.text_input("Name", value=entry["person"], key=f"name_{ts}")
        new_reason = st.text_input("Reason", value=entry["reason"], key=f"reason_{ts}")
        new_severity = st.slider("Severity", 0, 100, entry["severity"], key=f"severity_{ts}")

        if st.button("Save Changes", key=f"save_{ts}"):
            updated = {
                "person": new_person.strip(),
                "reason": new_reason.strip(),
                "severity": new_severity,
                "timestamp": ts
            }
            # Replace matching entry by timestamp
            heartbreaks = [
                updated if h["timestamp"] == ts else h
                for h in heartbreaks
            ]
            save_data(heartbreaks)
            st.success("Updated.")
            st.experimental_rerun()

        if st.button("Delete Entry", key=f"delete_{ts}"):
            # Filter out the entry by timestamp
            heartbreaks = [h for h in heartbreaks if h["timestamp"] != ts]
            save_data(heartbreaks)
            st.warning("Deleted.")
            st.experimental_rerun()


# --- Final Message if Maxed Out ---
if get_total_heartbreak(heartbreaks) >= 100:
    st.markdown("---")
    st.markdown(
        "<p style='color: darkred; font-size: 18px; text-align: center;'>"
        "I'm so sorry. You deserve to be loved. But I'm telling you, you are loved. "
        "Even if you feel you're alone, don't let your light go out. You're still here, "
        "and you're brave for doing that."
        "</p>",
        unsafe_allow_html=True
    )

