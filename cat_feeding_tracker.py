from tkinter import *
from tkcalendar import DateEntry
import matplotlib.pyplot as plt

# Used basic Tkinter GUI structure examples and class learning.
# My own code includes the cat feeding tracker idea based on my real-life problem.
# I used my cats' names and added food choices, date selection,
# feeding record display, vitamin tracking, and a food chart feature.

root = Tk()  # creates the main application window
root.iconbitmap("icons8-cat-100 (1).ico")  # adds cat icon to window
root.title("Cat Feeding Tracker")  # sets window title
root.geometry("550x600")  # sets window size

cat_names = ["Mew", "Nala", "Hime", "Doja", "Haru"]  # list of my cat names

food_types = [  # list of food options
    "Chicken & Quail Egg recipe in Broth",
    "Sardine",
    "Wild Salmon & Chicken",
    "Ahi Tuna & Chicken Recipe in Chicken Consomme"
]

vitamin_options = ["Yes", "No"]  # vitamin choices

selected_cat = StringVar()  # stores selected cat name
selected_cat.set(cat_names[0])  # default cat

selected_food = StringVar()  # stores selected food
selected_food.set(food_types[0])  # default food

selected_vitamin = StringVar()  # stores vitamin choice
selected_vitamin.set(vitamin_options[1])  # default vitamin choice

food_count = {}  # stores how many times each food was used

title_label = Label(root, text="🐾 Cat Feeding Tracker 🐾", font=("Calibri", 16))
title_label.pack()

cat_label = Label(root, text="Select Cat Name:")
cat_label.pack()

cat_menu = OptionMenu(root, selected_cat, *cat_names)
cat_menu.pack()

food_label = Label(root, text="Select Food Type:")
food_label.pack()

food_menu = OptionMenu(root, selected_food, *food_types)
food_menu.pack()

date_label = Label(root, text="Select Date:")
date_label.pack()

date_picker = DateEntry(root, width=20)
date_picker.pack()

vitamin_label = Label(root, text="Did you give vitamin?")
vitamin_label.pack()

vitamin_menu = OptionMenu(root, selected_vitamin, *vitamin_options)
vitamin_menu.pack()

record_label = Label(root, text="Feeding Record:")
record_label.pack()

record_box = Text(root, height=12, width=55)
record_box.pack()

def save_record():
    cat = selected_cat.get()
    food = selected_food.get()
    vitamin = selected_vitamin.get()
    selected_date = date_picker.get()

    note = ""
    if food in ["Ahi Tuna & Chicken Recipe in Chicken Consomme", "Wild Salmon & Chicken"]:
        note = " - Mixed dinner!"
    elif food == "Sardine":
        note = " - Fish day!"
    elif food == "Chicken & Quail Egg recipe in Broth":
        note = " - Chicken day!"

    record = selected_date + " - " + cat + " ate " + food + note + " - Vitamin: " + vitamin + "\n"
    record_box.insert(END, record)

    if food in food_count:
        food_count[food] += 1
    else:
        food_count[food] = 1

def clear_record():
    record_box.delete("1.0", END)

def show_chart():
    if not food_count:
        return

    foods = list(food_count.keys())
    counts = list(food_count.values())

    plt.bar(foods, counts)
    plt.title("Food Frequency")
    plt.xlabel("Food Type")
    plt.ylabel("Times Fed")
    plt.xticks(rotation=20)
    plt.show()

save_button = Button(root, text="Save Record", command=save_record)
save_button.pack()

clear_button = Button(root, text="Clear Record", command=clear_record)
clear_button.pack()

chart_button = Button(root, text="Show Food Chart", command=show_chart)
chart_button.pack()

root.mainloop()