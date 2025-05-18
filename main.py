import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Dummy task list (can be replaced with database)
task_data = []

# Caching example with CGPA and Score
@st.cache_data
def load_sample_data():
    df = pd.DataFrame({
        "Student": [f"Student {i+1}" for i in range(10)],
        "CGPA": [round(6 + i * 0.2, 2) for i in range(10)],
        "Score": [60 + i * 4 for i in range(10)]
    })
    st.table(df)
    st.success(st.json(df.to_json(orient="records")))
    return df
    

# Title
st.set_page_config(page_title="Task Manager", layout="wide")
st.title("🗂️ Task Manager Dashboard")

# Task Entry Form
with st.form("task_form"):
    st.subheader("📌 Add New Task")
    title = st.text_input("Task Title")
    description = st.text_area("Description")
    due_date = st.date_input("Due Date", datetime.date.today())
    submit = st.form_submit_button("Add Task")

    if submit:
        task_data.append({
            "Title": title,
            "Description": description,
            "Due Date": due_date.strftime("%Y-%m-%d")
        })
        st.success("✅ Task added successfully!")

# Show tasks if any
if task_data:
    st.subheader("📋 All Tasks")
    st.table(pd.DataFrame(task_data))

# JSON response simulation
if task_data:
    st.subheader("🧾 JSON Response")
    st.json(task_data)

# File Upload
st.subheader("📤 Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file:
    df_uploaded = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded data:")
    st.dataframe(df_uploaded)
    

# Cached Data Plot with CGPA vs Score
st.subheader("📈 CGPA vs Score Plot")
data = load_sample_data()
fig, ax = plt.subplots()
ax.bar(data["Student"], data["Score"], label="Score", alpha=0.6)
ax.plot(data["Student"], data["CGPA"], color='red', marker='o', label="CGPA", linewidth=2)
plt.xticks(rotation=45)
ax.set_ylabel("Score / CGPA")
ax.set_title("Student CGPA vs Score")
ax.legend()
st.pyplot(fig)
