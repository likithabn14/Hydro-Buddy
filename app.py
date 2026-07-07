import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

from data import (
    initialize_history,
    load_history,
    save_today,
    get_today_glasses,
    calculate_streak,
    weekly_history,
    get_mood
)

from reminder import (
    start_timer,
    get_countdown,
    should_show_reminder,
    random_message,
    drink_water,
    progress,
    goal_completed
)

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="💧 Hydro Buddy",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=1000, key="refresh")

initialize_history()

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

defaults = {
    "name": "Friend",
    "goal": 8,
    "glasses": get_today_glasses(),
    "interval": 30,
    "message": "Welcome! Stay Hydrated 💙",
    "buddy": "💧"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "last_drink" not in st.session_state:
    start_timer(st.session_state)

# -------------------------------------------------
# DARK THEME
# -------------------------------------------------

st.markdown("""
<style>

.stApp{
background:#05070B;
color:white;
}

header,
footer,
#MainMenu{
visibility:hidden;
}

.block-container{
padding-top:20px;
padding-left:35px;
padding-right:35px;
max-width:1450px;
}

.main-title{
font-size:52px;
font-weight:800;
color:white;
margin-bottom:5px;
}

.sub-title{
color:#8B949E;
font-size:18px;
margin-bottom:30px;
}

.card{
background:#111827;
border:1px solid #1F2937;
border-radius:20px;
padding:22px;
margin-bottom:20px;
}

.metric-card{
background:#111827;
border:1px solid #1F2937;
border-radius:18px;
padding:18px;
text-align:center;
}

.speech{
background:linear-gradient(90deg,#2563EB,#06B6D4);
padding:22px;
border-radius:18px;
font-size:24px;
font-weight:bold;
color:white;
}

.stButton>button{
width:100%;
background:#2563EB;
color:white;
border:none;
border-radius:12px;
padding:12px;
font-weight:bold;
}

.stButton>button:hover{
background:#0EA5E9;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------

hour = datetime.now().hour

if hour < 12:
    greeting = "🌞 Good Morning"
elif hour < 17:
    greeting = "☀️ Good Afternoon"
else:
    greeting = "🌙 Good Evening"

st.markdown("""
<div class="main-title">
💧 Hydro Buddy
</div>

<div class="sub-title">
Track your daily hydration and build healthy habits.
</div>
""", unsafe_allow_html=True)

st.success(f"{greeting}, {st.session_state.name}!")

# -------------------------------------------------
# USER SETTINGS
# -------------------------------------------------

with st.expander("⚙️ Personalize"):

    st.session_state.name = st.text_input(
        "Your Name",
        value=st.session_state.name
    )

    st.session_state.goal = st.slider(
        "Daily Goal",
        4,
        15,
        st.session_state.goal
    )

    st.session_state.interval = st.selectbox(
        "Reminder Every",
        [30,45,60],
        index=0
    )

    st.session_state.buddy = st.text_input(
        "Choose Your Buddy Emoji 😊🤖💧🐸",
        value=st.session_state.buddy,
        max_chars=2
    )

# -------------------------------------------------
# MAIN LAYOUT
# -------------------------------------------------

left, right = st.columns([1,3])

# -------------------------------------------------
# LEFT PANEL
# -------------------------------------------------

with left:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align:center;font-size:90px;">
        {st.session_state.buddy}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center;color:white;'>Your Hydro Buddy</h3>",
        unsafe_allow_html=True
    )

    st.write("")

    mood = get_mood(
        st.session_state.glasses,
        st.session_state.goal
    )

    if mood == "😴 Sleepy":
        mood_color = "#EF4444"

    elif mood == "😟 Worried":
        mood_color = "#F59E0B"

    elif mood == "😊 Happy":
        mood_color = "#10B981"

    else:
        mood_color = "#3B82F6"

    st.markdown(
        f"""
        <div style="
        background:{mood_color};
        padding:15px;
        border-radius:12px;
        text-align:center;
        color:white;
        font-size:20px;
        font-weight:bold;
        ">
        {mood}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    streak = calculate_streak(
        st.session_state.goal
    )

    st.metric(
        "🔥 Current Streak",
        f"{streak} Day(s)"
    )

    st.metric(
        "🎯 Daily Goal",
        f"{st.session_state.goal} Glasses"
    )

    st.metric(
        "💧 Water Today",
        st.session_state.glasses
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# RIGHT PANEL
# -------------------------------------------------

with right:

    st.markdown(
        f"""
        <div class="speech">

        {st.session_state.buddy} Hello {st.session_state.name}!

        <br><br>

        {st.session_state.message}

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    progress_value = progress(st.session_state)

    percent = int(progress_value * 100)

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "💧 Glasses",
            f"{st.session_state.glasses}/{st.session_state.goal}"
        )

    with c2:

        st.metric(
            "💙 Hydration",
            f"{percent}%"
        )

    with c3:

        st.metric(
            "🥤 Water",
            f"{st.session_state.glasses*250} ml"
        )

    st.progress(progress_value)

    st.write("")

    st.metric(
        "⏳ Next Reminder",
        get_countdown(st.session_state)
    )

    st.write("")

    btn1, btn2 = st.columns(2)

    with btn1:

        if st.button(
            "💧 I Drank Water",
            use_container_width=True
        ):

            drink_water(st.session_state)

            save_today(
                st.session_state.glasses
            )

            if goal_completed(st.session_state):

                st.balloons()

                st.success(
                    "🎉 Daily Goal Completed!"
                )

            st.rerun()

    with btn2:

        if st.button(
            "🔄 Reset Today",
            use_container_width=True
        ):

            st.session_state.glasses = 0

            start_timer(st.session_state)

            save_today(0)

            st.rerun()

# -------------------------------------------------
# REMINDER
# -------------------------------------------------

if should_show_reminder(st.session_state):

    st.warning("⏰ Time to Drink Water!")

    st.info(
        f"{st.session_state.buddy} {random_message()}"
    )

    # -------------------------------------------------
# HYDRO BUDDY SAYS
# -------------------------------------------------

st.write("")
st.markdown("## 💬 Hydro Buddy Says")

quotes = [

    "💧 Your body is asking for water.",

    "🚰 Don't let your bottle feel lonely.",

    "😊 Every sip makes you healthier.",

    "🌿 Staying hydrated improves focus.",

    "💙 Keep going! You're doing great.",

    "🥤 Water is the healthiest drink.",

    "⚡ Hydration keeps your energy high.",

    "🏃 Stay active. Stay hydrated."

]

st.markdown(
    f"""
    <div class="speech">
    {st.session_state.buddy} {random.choice(quotes)}
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# TODAY'S PROGRESS
# -------------------------------------------------

st.write("")
st.markdown("## 📊 Today's Progress")

progress_value = progress(st.session_state)

progress_percent = int(progress_value * 100)

remaining = max(
    0,
    st.session_state.goal - st.session_state.glasses
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "💧 Glasses",
        f"{st.session_state.glasses}/{st.session_state.goal}"
    )

with m2:
    st.metric(
        "🥤 Water",
        f"{st.session_state.glasses*250} ml"
    )

with m3:
    st.metric(
        "🚰 Remaining",
        remaining
    )

with m4:
    st.metric(
        "💙 Score",
        f"{progress_percent}%"
    )

st.progress(progress_value)

if progress_percent == 100:

    st.success("🏆 Congratulations! Daily goal completed!")

elif progress_percent >= 75:

    st.success("🔥 Almost there!")

elif progress_percent >= 50:

    st.info("💪 Great progress!")

else:

    st.warning("💧 Time for another glass!")


# -------------------------------------------------
# ACHIEVEMENTS
# -------------------------------------------------

st.write("")
st.markdown("## 🏆 Achievements")

badges=[]

if st.session_state.glasses>=1:
    badges.append("🥤 First Sip")

if st.session_state.glasses>=3:
    badges.append("💙 Hydration Starter")

if st.session_state.glasses>=5:
    badges.append("🌟 Water Lover")

if st.session_state.glasses>=st.session_state.goal:
    badges.append("🏅 Goal Crusher")

streak=calculate_streak(st.session_state.goal)

if streak>=3:
    badges.append("🔥 3-Day Streak")

if streak>=7:
    badges.append("👑 Weekly Champion")

if badges:

    cols=st.columns(3)

    for i,badge in enumerate(badges):

        with cols[i%3]:

            st.success(badge)

else:

    st.info("Drink water to unlock achievements!")

    # -------------------------------------------------
# WATER HISTORY
# -------------------------------------------------

st.write("")
st.markdown("## 📋 Water History")

history = load_history()

if not history.empty:

    history = history.sort_values(
        by="Date",
        ascending=False
    )

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )

    csv = history.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download History",
        csv,
        "HydroBuddy_History.csv",
        "text/csv",
        use_container_width=True
    )

else:

    st.info("No history available yet.")

# -------------------------------------------------
# DAILY HEALTH TIPS
# -------------------------------------------------

tips = [

    "💧 Drink a glass of water after waking up.",

    "🍋 Add lemon to your water for freshness.",

    "🧠 Staying hydrated improves concentration.",

    "🏃 Drink extra water after exercise.",

    "🌿 Water helps regulate body temperature.",

    "😊 Carry a reusable water bottle with you.",

    "⚡ Small sips throughout the day are better than drinking everything at once.",

    "❤️ Healthy habits begin with hydration."

]

st.write("")
st.markdown("## 💡 Daily Health Tip")

st.info(
    f"{st.session_state.buddy} {random.choice(tips)}"
)

# -------------------------------------------------
# QUICK SUMMARY
# -------------------------------------------------

st.write("")
st.markdown("## 📌 Today's Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "💧 Glasses",
        st.session_state.glasses
    )

with c2:

    st.metric(
        "🥤 Water",
        f"{st.session_state.glasses*250} ml"
    )

with c3:

    st.metric(
        "🔥 Streak",
        calculate_streak(st.session_state.goal)
    )

with c4:

    st.metric(
        "🎯 Goal",
        st.session_state.goal
    )

# -------------------------------------------------
# GOAL MESSAGE
# -------------------------------------------------

if goal_completed(st.session_state):

    st.success(
        f"{st.session_state.buddy} Congratulations! You completed today's hydration goal!"
    )

# -------------------------------------------------
# FLOATING HYDRO BUDDY
# -------------------------------------------------

st.markdown(f"""
<style>

.hydro-buddy{{

position:fixed;

bottom:25px;

right:25px;

background:#111827;

border:2px solid #2563EB;

border-radius:18px;

padding:18px;

width:240px;

color:white;

box-shadow:0px 0px 18px rgba(37,99,235,.5);

z-index:999;

}}

</style>

<div class="hydro-buddy">

<h2>{st.session_state.buddy}</h2>

<b>Hydro Buddy</b>

<hr>

Drink Water 💧

<br><br>

Stay Healthy ❤️

</div>

""", unsafe_allow_html=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.write("")
st.markdown("---")

st.markdown("""

<div style="text-align:center;color:#9CA3AF;">

💧 <b>Hydro Buddy</b>
<br>
Made with ❤️ using Streamlit <br><br>
Track • Hydrate • Stay Healthy
</div>

""", unsafe_allow_html=True)