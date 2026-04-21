# IMPORT LIBRARIES FOR APP, DATA HANDLING, AND CHART
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


# SET THE PAGE TITLE AND ICON THAT APPEARS IN THE BROWSER
st.set_page_config(page_title="Cat Feeding Tracker", page_icon="🐾")

# DISPLAY THE MAIN TITLE OF THE APP
st.title("🐾 Cat Feeding Tracker")

# SHORT DESCRIPTION OF THE APP
st.write("Track your cats' meals, vitamins, and feeding history.")

# LIST OF CAT NAMES USED IN THE APP
cat_names = ["Mew", "Nala", "Hime", "Doja", "Haru"]
cat_birth_year = {
    "Mew": 2017,
    "Nala": 2023,
    "Hime": 2023,
    "Doja": 2022,   
    "Haru": 2022    
}


# LIST OF FOOD OPTIONS AVAILABLE FOR THE CATS
food_types = [
    "Chicken & Quail Egg recipe in Broth",
    "Sardine",
    "Wild Salmon & Chicken",
    "Ahi Tuna & Chicken Recipe in Chicken Consomme"
]

# OPTIONS TO TRACK WHETHER VITAMIN WAS GIVEN
vitamin_options = ["Yes", "No"]
# OPTIONS FOR MEAL TIME ( new feature) 
meal_time_options = ["Breakfast", "Dinner"]

# CREATE STORAGE FOR RECORDS IF IT DOES NOT EXIST
if "records" not in st.session_state:
    st.session_state.records = []

# FUNCTION TO ASSIGN A NOTE BASED ON FOOD TYPE
def get_note(food_name):
    if food_name in ["Ahi Tuna & Chicken Recipe in Chicken Consomme", "Wild Salmon & Chicken"]:
        return "Mixed dinner!"
    elif food_name == "Sardine":
        return "Fish day!"
    elif food_name == "Chicken & Quail Egg recipe in Broth":
        return "Chicken day!"
    return ""

# SIDEBAR INPUT SECTION
st.sidebar.header("Add Feeding Record")

cat = st.sidebar.selectbox("Select Cat Name:", cat_names)
food = st.sidebar.selectbox("Select Food Type:", food_types)
selected_date = st.sidebar.date_input("Select Date:", value=date.today())
vitamin = st.sidebar.selectbox("Did you give vitamin?", vitamin_options)
meal_time = st.sidebar.selectbox("Select Meal Time:", meal_time_options)

# SAVE RECORD BUTTON
if st.sidebar.button("Save Record"):
    note = get_note(food)
  
   
    new_record = {
        "Date": str(selected_date),
        "Cat": cat,
        "Birth Year": cat_birth_year[cat],
        "Meal Time": meal_time, 
        "Food": food,
        "Note": note,
        "Vitamin": vitamin
    }
    st.session_state.records.append(new_record)
    st.success("Record saved!")

# CLEAR RECORDS BUTTON
if st.sidebar.button("Clear All Records"):
    st.session_state.records = []
    st.warning("All records cleared.")

# DISPLAY DATA IF RECORDS EXIST
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    df["Date"] = pd.to_datetime(df["Date"])

    # FILTER OPTION
    st.sidebar.header("Filter Options")
    selected_filter_cat = st.sidebar.selectbox(
        "Choose a cat to view records:",
        cat_names
    )

    filtered_df = df[df["Cat"] == selected_filter_cat]
 
    # DISPLAY ALL RECORDS
    st.subheader("Feeding Record")
    st.dataframe(df.reset_index(drop=True), use_container_width=True)

    # MEAL TYPE SUMMARY CHART
    st.subheader("Meal Type Summary")

    meal_summary = filtered_df["Note"].value_counts()
    meal_summary = meal_summary[meal_summary > 0]

    if not meal_summary.empty:
        fig, ax = plt.subplots()
        ax.pie(
            meal_summary.values,
            labels=meal_summary.index,
            autopct="%1.0f%%",
            startangle=90,
            wedgeprops={"edgecolor": "white"}
        )
        ax.set_title(f"{selected_filter_cat}'s Meal Types")
        st.pyplot(fig)
    else:
        st.info("No meal data available yet.")

else:
    st.info("No feeding records yet. Add one from the sidebar.")
