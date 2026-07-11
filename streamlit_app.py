import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import Habit_tracker
# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Smart Habit Tracker",
    page_icon="📊",
    layout="wide"
)
# ---------------- SIDEBAR ---------------- #
menu = st.sidebar.radio(
    "📂 Navigation",
    [
        "🏠 Home",
        "✅ Daily Tracking",
        "📊 Dashboard",
        "📈 Reports",
        "🔥 Streaks",
        "🏆 Achievements",
        "⚙️ Settings",
        "ℹ️ About"
    ]
)
# ---------------- DATA LOADER FOR DYNAMIC HOME ---------------- #
try:
    habit_percentage, best_habit, worst_habit = Habit_tracker.habit_performance_report()
    overall_productivity = Habit_tracker.productivity_score(habit_percentage)
    streaks = Habit_tracker.streak_report()
    max_streak = max([info["current"] for info in streaks.values()]) if streaks else 0
except Exception:
    habit_percentage, best_habit, worst_habit = {}, "None", "None"
    overall_productivity = 0.0
    streaks = {}
    max_streak = 0
# ---------------- HOME PAGE ---------------- #
if menu == "🏠 Home":
    st.title("🚀 Smart Habit Tracker")
    st.markdown("""
# Build Better Habits. Build a Better You.
Stay consistent, monitor your progress, analyze your performance,
and achieve your goals through intelligent habit tracking.
---
""")
    if st.button("🚀 Get Started"):
        st.success("Welcome! Use the sidebar to explore the application.")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📅 Habits Tracked", f"{len(Habit_tracker.habits)}")
    with col2:
        st.metric("🔥 Max Streak", f"{max_streak} Days")
    with col3:
        st.metric("🏆 Productivity Score", f"{overall_productivity:.2f}%")
    with col4:
        st.metric("📈 Overall Success", f"{overall_productivity:.2f}%")
    st.markdown("---")
    st.subheader("✨ Features")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### ✅ Daily Habit Tracking")
        st.write("Track your habits every day and build consistency.")
        st.markdown("### 📈 Productivity Reports")
        st.write("Generate daily, weekly and monthly reports.")
    with c2:
        st.markdown("### 📊 Smart Analytics")
        st.write("Visualize your progress using graphs and insights.")
        st.markdown("### 🏆 Achievement System")
        st.write("Unlock achievements based on your productivity.")
    st.markdown("---")
    st.subheader("💡 Why Smart Habit Tracker?")
    st.info("""
Unlike a basic checklist, Smart Habit Tracker helps you build consistency,
track productivity, visualize progress, and achieve long-term goals.
""")
    st.markdown("---")
    st.success(
        "💪 Small consistent actions repeated every day create extraordinary results."
    )
    st.markdown("---")
    st.caption("Developed by Sharan | Smart Habit Tracker v1.0")
# ---------------- DAILY TRACKING ---------------- #
elif menu == "✅ Daily Tracking":
    st.title("✅ Daily Tracking")
    st.subheader("Today's Habits")
    st.write("Mark the habits you completed today.")
    habits = Habit_tracker.habits
    daily_progress = {}
    # Form to select habits
    for habit in habits:
        completed = st.checkbox(habit, key=f"check_{habit}")
        if completed:
            daily_progress[habit] = "yes"
        else:
            daily_progress[habit] = "no"
    if st.button("💾 Save Today's Progress"):
        current_date = datetime.now().strftime("%d-%m-%Y")
        Habit_tracker.save_habit_data(current_date, daily_progress)
        (
            count_yes,
            count_no,
            total_habits,
            percentage,
            completed_habits,
            not_completed_habits
        ) = Habit_tracker.daily_summary(daily_progress)
        daily_productivity = Habit_tracker.daily_productivity(
            count_yes,
            total_habits,
            current_date
        )
        st.success("Today's progress saved successfully!")
        st.markdown("---")
        st.subheader("📅 Daily Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ Completed", count_yes)
        with col2:
            st.metric("❌ Not Completed", count_no)
        with col3:
            st.metric("📈 Completion", f"{percentage:.2f}%")
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### ✅ Completed Habits")
            if completed_habits:
                for habit in completed_habits:
                    st.write("✔", habit)
            else:
                st.write("*None*")
        with col_right:
            st.markdown("### ❌ Not Completed Habits")
            if not_completed_habits:
                for habit in not_completed_habits:
                    st.write("✖", habit)
            else:
                st.write("*None*")
# ---------------- DASHBOARD ---------------- #
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard")
    
    if not habit_percentage:
        st.info("No habit performance records found yet. Go to **Daily Tracking** to log your progress!")
    else:
        st.metric(
            "🏆 Overall Productivity",
            f"{overall_productivity:.2f}%"
        )
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🏆 Best Habit\n\n**{best_habit}**")
        with col2:
            st.error(f"⚠ Worst Habit\n\n**{worst_habit}**")
        st.markdown("---")
        st.subheader("🏅 Habit Rankings")
        rank = 1
        sorted_habits = sorted(habit_percentage.items(), key=lambda x: x[1], reverse=True)
        
        # Display rankings in grid columns
        cols = st.columns(2)
        for idx, (habit, percentage) in enumerate(sorted_habits):
            col_target = cols[idx % 2]
            col_target.write(f"{rank}. **{habit}** — {percentage:.2f}%")
            rank += 1
        st.markdown("---")
        st.subheader("📈 Habit Performance Graph")
        habit_names = [k for k, v in sorted_habits]
        success_percentage = [v for k, v in sorted_habits]
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Apply clean style elements to bar plot
        bars = ax.barh(habit_names, success_percentage, color="#1E88E5")
        ax.set_title("Habit Success Percentage", fontsize=14, fontweight='bold')
        ax.set_xlabel("Success Rate (%)", fontweight='bold')
        ax.set_ylabel("Habits", fontweight='bold')
        ax.set_xlim(0, 100)
        ax.grid(axis="x", linestyle="--", alpha=0.7)
        
        # Invert y-axis to show highest on top
        ax.invert_yaxis()
        
        # Add values inside bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                    va='center', ha='left', fontsize=9)
        st.pyplot(fig)
# ---------------- REPORTS ---------------- #
elif menu == "📈 Reports":
    st.title("📈 Reports")
    if not habit_percentage:
        st.info("No report details are generated. Start saving daily logs in **Daily Tracking**.")
    else:
        st.subheader("📅 Weekly Report")
        week1_average, week2_average, week3_average, week4_average = Habit_tracker.weekly_report()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Week 1", f"{week1_average:.2f}%")
        with col2:
            st.metric("Week 2", f"{week2_average:.2f}%")
        with col3:
            st.metric("Week 3", f"{week3_average:.2f}%")
        with col4:
            st.metric("Week 4", f"{week4_average:.2f}%")
        st.markdown("---")
        st.subheader("📆 Monthly Report")
        monthly_average = Habit_tracker.monthly_report(
            week1_average,
            week2_average,
            week3_average,
            week4_average
        )
        st.metric(
            "Overall Monthly Productivity",
            f"{monthly_average:.2f}%"
        )
        
        st.markdown("---")
        st.subheader("📊 Category Analysis")
        health_average, learning_average, self_average = Habit_tracker.category_analysis(habit_percentage)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "💪 Health",
                f"{health_average:.2f}%"
            )
        with col2:
            st.metric(
                "📚 Learning",
                f"{learning_average:.2f}%"
            )
        with col3:
            st.metric(
                "🌱 Self Development",
                f"{self_average:.2f}%"
            )
         
        st.markdown("---")
        st.subheader("⚠ Risk Detection")
        risk_data = Habit_tracker.risk_detection(habit_percentage)
        for habit, percentage, status in risk_data:
            if "High Risk" in status:
                st.error(f"❌ **{habit}**\n\n{status}\n\nSuccess Rate : {percentage:.2f}%")
            elif "Moderate" in status:
                st.warning(f"⚠ **{habit}**\n\n{status}\n\nSuccess Rate : {percentage:.2f}%")
            elif "Good" in status:
                st.info(f"ℹ **{habit}**\n\n{status}\n\nSuccess Rate : {percentage:.2f}%")
            else:
                st.success(f"✅ **{habit}**\n\n{status}\n\nSuccess Rate : {percentage:.2f}%")
# ---------------- STREAKS ---------------- #
elif menu == "🔥 Streaks":
    st.title("🔥 Habit Streaks")
    st.markdown("Consistency is the key. Complete your habits daily to grow your streaks!")
    if not streaks:
        st.info("No streaks logged. Start completing habits in **Daily Tracking** to build streaks!")
    else:
        active_streaks = {k: v for k, v in streaks.items() if v["current"] > 0}
        
        st.subheader("💡 Top Active Streaks")
        if active_streaks:
            sorted_active = sorted(active_streaks.items(), key=lambda x: x[1]["current"], reverse=True)
            cols = st.columns(min(len(sorted_active), 4))
            for idx, (habit, info) in enumerate(sorted_active[:4]):
                with cols[idx % 4]:
                    st.metric(
                        label=f"{habit}",
                        value=f"{info['current']} Days 🔥",
                        delta=f"Best: {info['longest']}d"
                    )
        else:
            st.warning("No active streaks right now. Complete a habit today to start a streak!")
        st.markdown("---")
        st.subheader("📋 All Habits Streaks")
        
        streak_table = []
        for habit, info in streaks.items():
            streak_table.append({
                "Habit Name": habit,
                "Current Streak 🔥": f"{info['current']} Days",
                "Longest Streak 🏆": f"{info['longest']} Days",
                "Status": "🔥 Active" if info['current'] > 0 else "❄ Inactive"
            })
        st.table(streak_table)
# ---------------- ACHIEVEMENTS ---------------- #
elif menu == "🏆 Achievements":
    st.title("🏆 Achievements & Milestones")
    st.markdown("Unlock milestones by improving your consistency score!")
    current_badge = Habit_tracker.achievement_system(overall_productivity)
    st.success(f"### Current Rank Achievement: **{current_badge}** (Overall Score: {overall_productivity:.2f}%)")
    st.markdown("---")
    st.subheader("🎖 Achievements List")
    badges = [
        {"name": "Legendary Achiever", "desc": "Maintain 95% or higher overall productivity score", "emoji": "👑", "min_score": 95},
        {"name": "Master of Consistency", "desc": "Maintain 90% or higher overall productivity score", "emoji": "🧙‍♂️", "min_score": 90},
        {"name": "Productivity Champion", "desc": "Maintain 80% or higher overall productivity score", "emoji": "🏆", "min_score": 80},
        {"name": "Rising Performer", "desc": "Maintain 70% or higher overall productivity score", "emoji": "🚀", "min_score": 70},
        {"name": "Getting Better", "desc": "Maintain 60% or higher overall productivity score", "emoji": "📈", "min_score": 60},
        {"name": "Never Give Up", "desc": "Start tracking your habits", "emoji": "💪", "min_score": 0}
    ]
    for badge in badges:
        is_unlocked = overall_productivity >= badge["min_score"]
        col1, col2 = st.columns([1, 6])
        with col1:
            if is_unlocked:
                st.markdown(f"<h1 style='text-align: center; margin: 0;'>{badge['emoji']}</h1>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h1 style='text-align: center; margin: 0; filter: grayscale(100%); opacity: 0.3;'>{badge['emoji']}</h1>", unsafe_allow_html=True)
        with col2:
            if is_unlocked:
                st.markdown(f"#### **{badge['name']}** <span style='color: #2E7D32; font-weight: bold;'>[UNLOCKED]</span>", unsafe_allow_html=True)
                st.write(badge["desc"])
            else:
                st.markdown(f"#### <span style='color: #757575;'>**{badge['name']}** [LOCKED]</span>", unsafe_allow_html=True)
                st.write(f"*{badge['desc']}*")
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
# ---------------- SETTINGS ---------------- #
elif menu == "⚙️ Settings":
    st.title("⚙️ Settings & Configuration")
    st.write("Manage your local configuration and export your tracking logs.")
    st.markdown("---")
    st.subheader("📥 Export History Data")
    st.write("Download your logs as a CSV file to backing up or analysis in other spreadsheet apps.")
    try:
        with open("Habit_tracker.txt", "r") as f:
            habit_csv = f.read()
        st.download_button(
            label="Download Habit Logs CSV",
            data=habit_csv,
            file_name="Habit_tracker.csv",
            mime="text/csv"
        )
    except FileNotFoundError:
        st.info("No habit history data file found to download.")
    try:
        with open("Daily_productivity.txt", "r") as f:
            prod_csv = f.read()
        st.download_button(
            label="Download Daily Productivity CSV",
            data=prod_csv,
            file_name="Daily_productivity.csv",
            mime="text/csv"
        )
    except FileNotFoundError:
        st.info("No productivity score file found.")
    st.markdown("---")
    st.subheader("⚠ Data Reset")
    st.write("Warning: Resetting data will permanently delete all logs.")
    confirm_reset = st.checkbox("Yes, I understand that this resets my streaks and logs.")
    if confirm_reset:
        if st.button("Permanently Clear Data Files"):
            import os
            cleared = []
            if os.path.exists("Habit_tracker.txt"):
                os.remove("Habit_tracker.txt")
                cleared.append("Habit_tracker.txt")
            if os.path.exists("Daily_productivity.txt"):
                os.remove("Daily_productivity.txt")
                cleared.append("Daily_productivity.txt")
            
            if cleared:
                st.success(f"Cleared records file: {', '.join(cleared)}.")
                st.info("Reload the page to start clean.")
            else:
                st.warning("No data files exist yet.")
# ---------------- ABOUT ---------------- #
elif menu == "ℹ️ About":
    st.title("ℹ️ About")
    st.write("""
### Smart Habit Tracker
**Developer:** Sharan
A Python and Streamlit based productivity application.
### Features
- **Daily Habit Tracking**: Tick your achievements every day.
- **Productivity Analysis**: Instantly compute your completion status.
- **Weekly & Monthly Reports**: Track category averages over weeks.
- **Habit Streaks**: Monitor continuous habit completions.
- **Smart Analytics**: Visualization of progress using Horizontal Bar charts.
- **Achievement System**: Badge unlocks based on consistency.
""")