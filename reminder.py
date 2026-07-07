from datetime import datetime, timedelta
import random

# --------------------------------------------------
# Reminder Messages
# --------------------------------------------------

REMINDER_MESSAGES = [
    "💧 Your body is asking for water.",
    "🥤 Hydration break! Time for a sip.",
    "🌿 Water keeps your mind fresh.",
    "💙 Future you will thank you.",
    "🚰 Don't let your water bottle feel lonely.",
    "✨ Stay hydrated. Stay awesome.",
    "😊 Every sip counts!",
    "🧠 Water helps you stay focused.",
    "❤️ Your body deserves some water.",
    "🌊 Refresh yourself with a glass of water."
]


# --------------------------------------------------
# Start Timer
# --------------------------------------------------

def start_timer(session_state):
    """
    Starts or restarts the reminder timer.
    """

    session_state.last_drink = datetime.now()
    session_state.popup = False


# --------------------------------------------------
# Remaining Time
# --------------------------------------------------

def get_remaining_time(session_state):
    """
    Returns remaining seconds before reminder.
    """

    next_time = session_state.last_drink + timedelta(
        minutes=session_state.interval
    )

    remaining = (next_time - datetime.now()).total_seconds()

    return max(0, int(remaining))


# --------------------------------------------------
# Countdown Text
# --------------------------------------------------

def get_countdown(session_state):
    """
    Returns countdown as MM:SS
    """

    seconds = get_remaining_time(session_state)

    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:02}:{seconds:02}"


# --------------------------------------------------
# Reminder Check
# --------------------------------------------------

def should_show_reminder(session_state):
    """
    True if reminder should be displayed.
    """

    return get_remaining_time(session_state) == 0


# --------------------------------------------------
# Reminder Message
# --------------------------------------------------

def random_message():
    return random.choice(REMINDER_MESSAGES)


# --------------------------------------------------
# Drink Water
# --------------------------------------------------

def drink_water(session_state):
    """
    Updates timer after drinking water.
    """

    session_state.glasses += 1

    session_state.last_drink = datetime.now()

    session_state.popup = False

    session_state.message = random_message()


# --------------------------------------------------
# Progress
# --------------------------------------------------

def progress(session_state):
    if session_state.goal == 0:
        return 0

    return min(
        session_state.glasses / session_state.goal,
        1.0
    )


# --------------------------------------------------
# Goal Check
# --------------------------------------------------

def goal_completed(session_state):
    return session_state.glasses >= session_state.goal