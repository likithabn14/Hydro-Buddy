import os
from datetime import datetime, timedelta
import pandas as pd

HISTORY_FILE = "history.csv"


# ---------------------------------------------------
# CREATE HISTORY FILE IF NOT EXISTS
# ---------------------------------------------------

def initialize_history():
    if not os.path.exists(HISTORY_FILE):
        df = pd.DataFrame(columns=["Date", "Glasses"])
        df.to_csv(HISTORY_FILE, index=False)


# ---------------------------------------------------
# LOAD HISTORY
# ---------------------------------------------------

def load_history():
    initialize_history()
    return pd.read_csv(HISTORY_FILE)


# ---------------------------------------------------
# SAVE TODAY'S DATA
# ---------------------------------------------------

def save_today(glasses):
    initialize_history()

    today = datetime.now().strftime("%Y-%m-%d")

    df = pd.read_csv(HISTORY_FILE)

    if today in df["Date"].values:
        df.loc[df["Date"] == today, "Glasses"] = glasses
    else:
        df.loc[len(df)] = [today, glasses]

    df.to_csv(HISTORY_FILE, index=False)


# ---------------------------------------------------
# GET TODAY'S GLASSES
# ---------------------------------------------------

def get_today_glasses():
    initialize_history()

    today = datetime.now().strftime("%Y-%m-%d")

    df = pd.read_csv(HISTORY_FILE)

    row = df[df["Date"] == today]

    if row.empty:
        return 0

    return int(row.iloc[0]["Glasses"])


# ---------------------------------------------------
# CALCULATE STREAK
# ---------------------------------------------------

def calculate_streak(goal):
    initialize_history()

    df = pd.read_csv(HISTORY_FILE)

    if df.empty:
        return 0

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    streak = 0
    expected = datetime.now().date()

    for _, row in df.iloc[::-1].iterrows():

        day = row["Date"].date()

        if day != expected:
            break

        if row["Glasses"] >= goal:
            streak += 1
            expected = expected - timedelta(days=1)
        else:
            break

    return streak


# ---------------------------------------------------
# WEEKLY HISTORY
# ---------------------------------------------------

def weekly_history(days=7):
    initialize_history()

    df = pd.read_csv(HISTORY_FILE)

    if df.empty:
        return pd.DataFrame(columns=["Date", "Glasses"])

    df["Date"] = pd.to_datetime(df["Date"])

    start = datetime.now() - timedelta(days=days - 1)

    df = df[df["Date"] >= start]

    return df.sort_values("Date")


# ---------------------------------------------------
# GOAL COMPLETED
# ---------------------------------------------------

def goal_completed(glasses, goal):
    return glasses >= goal


# ---------------------------------------------------
# MOOD
# ---------------------------------------------------

def get_mood(glasses, goal):

    if glasses == 0:
        return "😴 Sleepy"

    elif glasses <= 2:
        return "😟 Worried"

    elif glasses < goal:
        return "😊 Happy"

    else:
        return "🥳 Celebration"


# ---------------------------------------------------
# RANDOM REMINDER MESSAGES
# ---------------------------------------------------

MESSAGES = [
    "💧 Your body is asking for water.",
    "🥤 Hydration break!",
    "💙 Future you will thank you.",
    "🌿 Stay refreshed with a glass of water.",
    "🚰 Don't let your water bottle feel lonely.",
    "✨ Every sip counts.",
    "😊 Keep yourself hydrated.",
    "🧠 Water helps you stay focused.",
    "💪 Your body loves hydration.",
    "❤️ One more glass and you're closer to your goal!"
]