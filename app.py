import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Cat Feeding Tracker", page_icon="🐾")

st.title("🐾 Cat Feeding Tracker")
st.write("Track your cats' meals, vitamins, and weekly feeding history.")

cat_names = ["Mew", "Nala", "Hime", "Doja", "Haru"]

food_types = [
    "Chicken & Quail Egg recipe in Broth",
    "Sardine",
    "Wild Salmon & Chicken",
    "Ahi Tuna & Chicken Recipe in Chicken Consomme"
]

vitamin_options = ["Yes", "No"]

if "records" not in st.session_state:
    st.session_state.records = []

def get_note(food_name):
    if food_name in ["Ahi Tuna & Chicken Recipe in Chicken Consomme", "Wild Salmon & Chicken"]:
        return "Mixed dinner!"
    elif food_name == "Sardine":
        return "Fish day!"
    elif food_name == "Chicken & Quail Egg recipe in Broth":
        return "Chicken day!"
    return ""

# Sidebar
st.sidebar.header("Add Feeding Record")

cat = st.sidebar.selectbox("Select Cat Name:", cat_names)
food = st.sidebar.selectbox("Select Food Type:", food_types)
selected_date = st.sidebar.date_input("Select Date:", value=date.today())
vitamin = st.sidebar.selectbox("Did you give vitamin?", vitamin_options)

if st.sidebar.button("Save Record"):
    note = get_note(food)
    new_record = {
        "Date": str(selected_date),
        "Cat": cat,
        "Food": food,
        "Note": note,
        "Vitamin": vitamin
    }
    st.session_state.records.append(new_record)
    st.success("Record saved!")

if st.sidebar.button("Clear All Records"):
    st.session_state.records = []
    st.warning("All records cleared.")

if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    df["Date"] = pd.to_datetime(df["Date"])

    st.sidebar.header("Filter Options")
    selected_filter_cat = st.sidebar.selectbox(
        "Choose a cat to view records:",
        ["All"] + cat_names
    )

    if selected_filter_cat == "All":
        filtered_df = df
    else:
        filtered_df = df[df["Cat"] == selected_filter_cat]

    st.subheader("Feeding Record")
    st.dataframe(filtered_df, use_container_width=True)

    # Food summary by selected cat
    st.subheader("Food Summary")

    if not filtered_df.empty:
        food_summary = filtered_df["Food"].value_counts().reindex(food_types, fill_value=0)

        summary_df = pd.DataFrame({
            "Food Type": food_summary.index,
            "Times Eaten": food_summary.values
        })

        st.dataframe(summary_df, use_container_width=True)

        fig_food, ax_food = plt.subplots()
        ax_food.bar(food_summary.index, food_summary.values)
        ax_food.set_title(f"Food Count for {selected_filter_cat}" if selected_filter_cat != "All" else "Food Count for All Cats")
        ax_food.set_xlabel("Food Type")
        ax_food.set_ylabel("Times Eaten")
        plt.xticks(rotation=20)
        st.pyplot(fig_food)
    else:
        st.info("No feeding records for this cat yet.")

    # Weekly tracker by cat
    st.subheader("Weekly Feeding Tracker by Cat")

    today = pd.Timestamp.today()
    start_of_week = today - pd.Timedelta(days=today.weekday())
    end_of_week = start_of_week + pd.Timedelta(days=6)

    weekly_df = df[(df["Date"] >= start_of_week) & (df["Date"] <= end_of_week)]
    weekly_count = weekly_df["Cat"].value_counts().reindex(cat_names, fill_value=0)

    fig_weekly, ax_weekly = plt.subplots()
    ax_weekly.bar(weekly_count.index, weekly_count.values)
    ax_weekly.set_title("Weekly Feeding Tracker by Cat")
    ax_weekly.set_xlabel("Cat Name")
    ax_weekly.set_ylabel("Times Fed This Week")
    plt.xticks(rotation=0)
    st.pyplot(fig_weekly)

else:
    st.info("No feeding records yet. Add one from the sidebar.")
