import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Employee Attendance Report", layout="wide")

st.title("📊 Employee Attendance Report - April 2025")

# Load CSV file
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Show Data Table
    st.subheader("📋 Attendance Table")
    # st.dataframe(df)

    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    st.write("Data Type of Date Column:", df)

#     # Summary statistics
    st.subheader("📈 Summary Statistics")
    summary = df.groupby("Status").size().reset_index(name="Count")
    summary["Total"]= df["Status"].count()
    st.write(summary)

#     # Attendance count per employee
    attendance_count = df[df["Status"] == "Present"].groupby("Employee ID").size()
    
    st.subheader("👨‍💼 Employees by Attendance")
    st.write(attendance_count.sort_index().reset_index(name="Days Present"))


    # Leave & No Show pie chart
    st.subheader("📌 Leave & No Show Distribution")
    leave_no_show = df[df["Status"] != "Present"]["Status"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(leave_no_show, labels=leave_no_show.index, autopct='%1.1f%%', startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

    # Daily attendance trend
    st.subheader("📅 Daily Attendance Trend")
    daily_trend = df[df["Status"] == "Present"].groupby("Date").size()

    fig2, ax2 = plt.subplots()
    sns.lineplot(x=daily_trend.index, y=daily_trend.values, ax=ax2)
    ax2.set_title("Number of Present Employees per Day")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Employees Present")
    plt.xticks(rotation=90)
    st.pyplot(fig2)

    # Heatmap of attendance frequency
    st.subheader("🔍 Heatmap of Employee Attendance")
    pivot = df[df["Status"] == "Present"].pivot_table(index="Employee ID", columns="Date", values="Status", aggfunc='count').fillna(0)
    fig3, ax3 = plt.subplots(figsize=(15, 8))
    sns.heatmap(pivot, cmap="YlGnBu", ax=ax3, cbar_kws={'label': 'Days Present'})
    st.pyplot(fig3)
    # Compute attendance counts for each employee
    attendance_summary = df.groupby(["Employee ID", "Status"]).size().unstack(fill_value=0)

    # Calculate total working days
    attendance_summary["Total Days"] = attendance_summary.sum(axis=1)
    # st.write(attendance_summary)

    # Calculate attendance index (%)
    attendance_summary["Attendance Index (%)"] = (
        (attendance_summary.get("Present", 0) + attendance_summary.get("Leave", 0)) 
        / attendance_summary["Total Days"]
    ) * 100

    attendance_summary = attendance_summary.sort_index()

    # Show the table
    st.subheader("✅ Employee Attendance Index (%)")
    st.dataframe(attendance_summary[["Present", "Leave", "No Show", "Total Days", "Attendance Index (%)"]])

    # Plot attendance index
    st.subheader("📊 Attendance Index Visualization")

    top_n = st.slider("Select number of employees to show", min_value=5, max_value=100, value=20)

    plot_data = attendance_summary["Attendance Index (%)"].sort_values(ascending=False).head(top_n)

    st.bar_chart(plot_data)

    # 🚨 Identify defaulters (more than 3 No Show days)
    defaulters = attendance_summary[attendance_summary["No Show"] > 3]

    # Show defaulter list
    if not defaulters.empty:
        st.subheader("🚨 Defaulter Employees (More than 3 No Show days)")
        st.dataframe(defaulters[["Present", "Leave", "No Show", "Total Days", "Attendance Index (%)"]])

        st.subheader("🚨 Defaulter Employees (More than 3 No Show days)")
        st.dataframe(defaulters[["Present", "Leave", "No Show", "Total Days", "Attendance Index (%)"]])
        
        # Create a bar chart of No Show counts for defaulters
        st.subheader("📉 Defaulters No Show Bar Chart")
        st.bar_chart(defaulters["No Show"].sort_values(ascending=False))
    else:
        st.success("🎉 No defaulters found! All employees have 3 or fewer No Show days.")

else:
    st.info("Please upload the attendance CSV file to begin.")


