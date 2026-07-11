import matplotlib.pyplot as plt
from datetime import datetime

# List of habits/tasks to be tracked daily

habits = [
    "Wake Up Early",
    "Drink 3-4 Litres of Water",
    "15 Minutes Yoga / Stretching",
    "Gratitude Writing",
    "Coding Practice",
    "Skill Building / Learning",
    "Work / College Tasks",
    "Screen Time Control",
    "Gym Workout",
    "Daily Protein Intake",
    "Healthy Meals",
    "Reading Books",
    "Daily Reflection / Review",
    "Outdoor Sports (Saturday & Sunday)"
]

# ---------------- DAILY TRACKING ---------------- #

def daily_tracking():
    print("=" * 50)
    print("         DAILY HABIT TRACKER")
    print("=" * 50)

    # Getting and displaying the current date and day
    current_date = datetime.now().strftime("%d-%m-%Y")
    today_day = datetime.now().strftime("%A")

    print("Today's Date :", current_date)
    print("Day :", today_day)

    daily_progress = {}

    for i in habits:
        if i == "Outdoor Sports (Saturday & Sunday)":
            if today_day != "Saturday" and today_day != "Sunday":
                continue

        while True:
            # Taking input from the user for each habit/task
            print("\nHabit / Task :", i)
            status = input("Did you complete it? (yes/no) : ").lower()

            if status == "yes" or status == "no":
                # Storing the completion status
                daily_progress[i] = status
                break
            else:
                print("Enter only yes or no")

    return daily_progress, current_date, today_day


# ---------------- SAVE DATA ---------------- #

def save_habit_data(current_date, daily_progress):
    try:
        with open("Habit_tracker.txt", "a") as file:
            for habit, status in daily_progress.items():
                file.write(f"{current_date},{habit},{status}\n")
        print("\nDaily habit progress saved successfully!")
    except Exception as e:
        print(f"Error saving habit data: {e}")


# ---------------- FUNCTION CALLS (DISABLED ON IMPORT) ---------------- #

# daily_progress, current_date, today_day = daily_tracking()
# save_habit_data(current_date, daily_progress)


# ---------------- DAILY SUMMARY ---------------- #

def daily_summary(daily_progress):
    print("\n" + "=" * 50)
    print("             DAILY SUMMARY")
    print("=" * 50)

    completed_habits = []
    not_completed_habits = []

    count_yes = 0
    count_no = 0

    for habit, status in daily_progress.items():
        if status == "yes":
            count_yes += 1
            completed_habits.append(habit)
        else:
            count_no += 1
            not_completed_habits.append(habit)

    total_habits = len(daily_progress)

    # Calculating today's completion percentage
    percentage = (count_yes / total_habits) * 100 if total_habits > 0 else 0.0

    print("Completion Percentage :", round(percentage, 2), "%")
    print("\nCompleted Habits :")
    for habit in completed_habits:
        print(habit)

    print("\nNot Completed Habits :")
    for habit in not_completed_habits:
        print(habit)

    return (
        count_yes,
        count_no,
        total_habits,
        percentage,
        completed_habits,
        not_completed_habits
    )


# ---------------- DISPLAY HABIT HISTORY ---------------- #

def display_habit_history():
    print("\n" + "=" * 50)
    print("             HABIT HISTORY")
    print("=" * 50)
    try:
        with open("Habit_tracker.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) != 3:
                    continue
                date = data[0]
                habit = data[1]
                status = data[2]

                print("Date :", date)
                print("Habit :", habit)
                print("Status :", status)
                print("-" * 40)
    except FileNotFoundError:
        print("No habit history found yet. File 'Habit_tracker.txt' does not exist.")


# ---------------- HABIT PERFORMANCE REPORT ---------------- #

def habit_performance_report():
    # Generating the habit performance report
    # Calculating total occurrences, completed counts, and success rates
    habit_total = {}
    habit_completed = {}

    try:
        with open("Habit_tracker.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) != 3:
                    continue
                date = data[0]
                habit = data[1]
                status = data[2]

                if habit not in habit_total:
                    habit_total[habit] = 0
                    habit_completed[habit] = 0

                habit_total[habit] += 1
                if status == "yes":
                    habit_completed[habit] += 1
    except FileNotFoundError:
        pass

    habit_percentage = {}
    for habit in habit_total:
        total = habit_total[habit]
        completed = habit_completed[habit]
        percentage = (completed / total) * 100
        habit_percentage[habit] = percentage

    # Identify the best performing habit
    best_habit = "None"
    best_percentage = -1
    for habit in habit_percentage:
        if habit_percentage[habit] > best_percentage:
            best_percentage = habit_percentage[habit]
            best_habit = habit

    # Identify the worst performing habit
    worst_habit = "None"
    worst_percentage = 101
    for habit in habit_percentage:
        if habit_percentage[habit] < worst_percentage:
            worst_percentage = habit_percentage[habit]
            worst_habit = habit

    print("\n" + "=" * 50)
    print("        BEST & WORST HABITS")
    print("=" * 50)
    print("\nBest Habit :", best_habit)
    print("Success Rate :", round(best_percentage, 2) if best_percentage >= 0 else 0.0, "%")
    print("\nWorst Habit :", worst_habit)
    print("Success Rate :", round(worst_percentage, 2) if worst_percentage <= 100 else 0.0, "%")

    print("\n" + "=" * 50)
    print("        HABIT PERFORMANCE REPORT")
    print("=" * 50)

    for habit in habit_total:
        total = habit_total[habit]
        completed = habit_completed[habit]
        percentage = (completed / total) * 100
        print("\nHabit :", habit)
        print("Completed :", completed)
        print("Total Tracked :", total)
        print("Success Rate :", round(percentage, 2), "%")

    return habit_percentage, best_habit, worst_habit


# ---------------- HABIT STREAK REPORT ---------------- #

def streak_report():
    # Calculating the current streak and longest streak for each habit
    habit_history = {}

    try:
        with open("Habit_tracker.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) != 3:
                    continue
                date = data[0]
                habit = data[1]
                status = data[2]

                if habit not in habit_history:
                    habit_history[habit] = []
                habit_history[habit].append(status)
    except FileNotFoundError:
        pass

    print("\n" + "=" * 50)
    print("           HABIT STREAK REPORT")
    print("=" * 50)

    streaks_dict = {}

    for habit in habit_history:
        history = habit_history[habit]
        current_streak = 0
        longest_streak = 0

        for status in history:
            if status == "yes":
                current_streak += 1
                if current_streak > longest_streak:
                    longest_streak = current_streak
            else:
                current_streak = 0

        today_streak = 0
        for status in reversed(history):
            if status == "yes":
                today_streak += 1
            else:
                break

        print("\nHabit :", habit)
        print("Current Streak :", today_streak, "days")
        print("Longest Streak :", longest_streak, "days")

        streaks_dict[habit] = {
            "current": today_streak,
            "longest": longest_streak
        }

    return streaks_dict


# ---------------- HABIT RANKING ---------------- #

def habit_ranking(habit_percentage):
    print("\n" + "=" * 50)
    print("          HABIT RANKING")
    print("=" * 50)

    rank = 1
    for habit in sorted(habit_percentage, key=habit_percentage.get, reverse=True):
        print(rank, ".", habit)
        print("Success Rate :", round(habit_percentage[habit], 2), "%")
        print("-" * 40)
        rank += 1


# ---------------- HABIT PERFORMANCE GRAPH ---------------- #

def performance_graph(habit_percentage):
    if not habit_percentage:
        print("No habit performance data to graph.")
        return

    print("\n" + "=" * 50)
    print("         HABIT PERFORMANCE GRAPH")
    print("=" * 50)

    habit_names = []
    success_percentage = []

    for habit in habit_percentage:
        habit_names.append(habit)
        success_percentage.append(habit_percentage[habit])

    plt.figure(figsize=(12,7))
    plt.barh(habit_names, success_percentage)
    plt.title("Habit Success Percentage")
    plt.xlabel("Success Percentage")
    plt.ylabel("Habits")
    plt.xlim(0,100)
    plt.grid(axis="x")
    plt.tight_layout()
    plt.show()


# ---------------- PRODUCTIVITY SCORE ---------------- #

def productivity_score(habit_percentage):
    print("\n" + "=" * 50)
    print("         PRODUCTIVITY SCORE")
    print("=" * 50)

    if not habit_percentage:
        print("Overall Productivity Score : 0.0 %")
        return 0.0

    total_score = 0
    for habit in habit_percentage:
        total_score += habit_percentage[habit]

    total_habits = len(habit_percentage)
    productivity_score = total_score / total_habits

    print("Overall Productivity Score :", round(productivity_score, 2), "%")
    return productivity_score


# ---------------- CATEGORY ANALYSIS ---------------- #

def category_analysis(habit_percentage):
    # Creating categories
    health = [
        "Wake Up Early",
        "Drink 3-4 Litres of Water",
        "15 Minutes Yoga / Stretching",
        "Gym Workout",
        "Daily Protein Intake",
        "Healthy Meals",
        "Outdoor Sports (Saturday & Sunday)"
    ]

    learning = [
        "Coding Practice",
        "Skill Building / Learning",
        "Reading Books"
    ]

    self_development = [
        "Gratitude Writing",
        "Work / College Tasks",
        "Screen Time Control",
        "Daily Reflection / Review"
    ]

    health_total = 0
    learning_total = 0
    self_total = 0

    health_count = 0
    learning_count = 0
    self_count = 0

    for habit in habit_percentage:
        if habit in health:
            health_total += habit_percentage[habit]
            health_count += 1
        elif habit in learning:
            learning_total += habit_percentage[habit]
            learning_count += 1
        elif habit in self_development:
            self_total += habit_percentage[habit]
            self_count += 1

    health_average = health_total / health_count if health_count > 0 else 0.0
    learning_average = learning_total / learning_count if learning_count > 0 else 0.0
    self_average = self_total / self_count if self_count > 0 else 0.0

    print("\n" + "=" * 50)
    print("        CATEGORY ANALYSIS")
    print("=" * 50)
    print("\nHealth")
    print("Average Score :", round(health_average, 2), "%")
    print("\nLearning")
    print("Average Score :", round(learning_average, 2), "%")
    print("\nSelf Development")
    print("Average Score :", round(self_average, 2), "%")

    return health_average, learning_average, self_average


# ---------------- RISK DETECTION ---------------- #

def risk_detection(habit_percentage):
    risk_data = []

    print("\n" + "=" * 50)
    print("           RISK DETECTION")
    print("=" * 50)

    for habit in habit_percentage:
        percentage = habit_percentage[habit]
        print("\nHabit :", habit)
        print("Success Rate :", round(percentage, 2), "%")

        if percentage < 50:
            status = "High Risk - Immediate Improvement Needed"
        elif percentage < 75:
            status = "Moderate Improvement Needed"
        elif percentage < 90:
            status = "Good Progress"
        else:
            status = "Excellent Consistency"

        print("Status :", status)
        print("-" * 40)
        risk_data.append((habit, percentage, status))

    return risk_data


# ---------------- DAILY PRODUCTIVITY SCORE ---------------- #

def daily_productivity(count_yes, total_habits, current_date):
    daily_prod = (count_yes / total_habits) * 100 if total_habits > 0 else 0.0

    print("\n" + "=" * 50)
    print("      DAILY PRODUCTIVITY SCORE")
    print("=" * 50)
    print("Today's Productivity Score :", round(daily_prod, 2), "%")

    try:
        with open("Daily_productivity.txt", "a") as file:
            file.write(f"{current_date},{round(daily_prod, 2)}\n")
    except Exception as e:
        print(f"Error saving daily productivity: {e}")

    return daily_prod


# ---------------- WEEKLY REPORT ---------------- #

def weekly_report():
    week1_total = 0
    week2_total = 0
    week3_total = 0
    week4_total = 0

    week1_days = 0
    week2_days = 0
    week3_days = 0
    week4_days = 0

    try:
        with open("Daily_productivity.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) != 2:
                    continue
                date = data[0]
                score = float(data[1])

                day = int(date.split("-")[0])

                if day >= 1 and day <= 7:
                    week1_total += score
                    week1_days += 1
                elif day >= 8 and day <= 14:
                    week2_total += score
                    week2_days += 1
                elif day >= 15 and day <= 21:
                    week3_total += score
                    week3_days += 1
                else:
                    week4_total += score
                    week4_days += 1
    except FileNotFoundError:
        pass

    week1_average = week1_total / week1_days if week1_days > 0 else 0.0
    week2_average = week2_total / week2_days if week2_days > 0 else 0.0
    week3_average = week3_total / week3_days if week3_days > 0 else 0.0
    week4_average = week4_total / week4_days if week4_days > 0 else 0.0

    print("\n" + "=" * 50)
    print("           WEEKLY REPORT")
    print("=" * 50)
    print("Week 1 :", round(week1_average, 2), "%")
    print("Week 2 :", round(week2_average, 2), "%")
    print("Week 3 :", round(week3_average, 2), "%")
    print("Week 4 :", round(week4_average, 2), "%")

    return week1_average, week2_average, week3_average, week4_average


# ---------------- MONTHLY REPORT ---------------- #

def monthly_report(week1_average, week2_average, week3_average, week4_average):
    print("\n" + "=" * 50)
    print("          MONTHLY REPORT")
    print("=" * 50)

    monthly_total = week1_average + week2_average + week3_average + week4_average
    monthly_average = monthly_total / 4

    print("Monthly Productivity Score :", round(monthly_average, 2), "%")
    return monthly_average


# ---------------- PRODUCTIVITY INSIGHTS ---------------- #

def productivity_insights(monthly_average, health_average, learning_average, self_average):
    print("\n" + "=" * 50)
    print("        PRODUCTIVITY INSIGHTS")
    print("=" * 50)

    # Overall Productivity Insight
    print("\nOverall Productivity :", round(monthly_average, 2), "%")

    if monthly_average >= 90:
        print("Excellent Productivity! Keep it up.")
    elif monthly_average >= 75:
        print("Good Productivity. Try to improve further.")
    else:
        print("Your Productivity Needs Improvement.")

    # Finding the strongest category
    best_category = "Health"
    best_score = health_average

    if learning_average > best_score:
        best_score = learning_average
        best_category = "Learning"

    if self_average > best_score:
        best_score = self_average
        best_category = "Self Development"

    # Finding the weakest category
    worst_category = "Health"
    worst_score = health_average

    if learning_average < worst_score:
        worst_score = learning_average
        worst_category = "Learning"

    if self_average < worst_score:
        worst_score = self_average
        worst_category = "Self Development"

    print("\nStrongest Category :", best_category)
    print("Average Score :", round(best_score, 2), "%")
    print("\nWeakest Category :", worst_category)
    print("Average Score :", round(worst_score, 2), "%")

    print("\nOverall Insight :")
    if monthly_average >= 90:
        print("You are maintaining excellent consistency across your habits.")
    elif monthly_average >= 75:
        print("You are doing well. Focus more on your weaker habits.")
    else:
        print("Try to improve your daily consistency and complete more habits.")


# ---------------- ACHIEVEMENT SYSTEM ---------------- #

def achievement_system(monthly_average):
    print("\n" + "=" * 50)
    print("         ACHIEVEMENT SYSTEM")
    print("=" * 50)
    print("\nMonthly Productivity :", round(monthly_average, 2), "%")

    if monthly_average >= 95:
        ach = "Legendary Achiever"
    elif monthly_average >= 90:
        ach = "Master of Consistency"
    elif monthly_average >= 80:
        ach = "Productivity Champion"
    elif monthly_average >= 70:
        ach = "Rising Performer"
    elif monthly_average >= 60:
        ach = "Getting Better"
    else:
        ach = "Never Give Up"

    print("Achievement :", ach)
    return ach


# ---------------- MAIN FUNCTION (FOR CLI MODE) ---------------- #

def main():
    # Daily Tracking
    daily_progress, current_date, today_day = daily_tracking()

    # Save Today's Data
    save_habit_data(current_date, daily_progress)

    # Daily Summary
    count_yes, count_no, total_habits, percentage, completed, not_completed = daily_summary(daily_progress)

    # Display Previous Habit History
    display_habit_history()

    # Habit Performance Report
    habit_percentage, best_habit, worst_habit = habit_performance_report()

    # Streak Report
    streak_report()

    # Habit Ranking
    habit_ranking(habit_percentage)

    # Performance Graph
    # performance_graph(habit_percentage)

    # Productivity Score
    productivity = productivity_score(habit_percentage)

    # Category Analysis
    health_average, learning_average, self_average = category_analysis(habit_percentage)

    # Risk Detection
    risk_detection(habit_percentage)

    # Daily Productivity
    daily_productivity_score = daily_productivity(count_yes, total_habits, current_date)

    # Weekly Report
    week1_average, week2_average, week3_average, week4_average = weekly_report()

    # Monthly Report
    monthly_average = monthly_report(week1_average, week2_average, week3_average, week4_average)

    # Productivity Insights
    productivity_insights(monthly_average, health_average, learning_average, self_average)

    # Achievement System
    achievement_system(monthly_average)


if __name__ == "__main__":
    main()
