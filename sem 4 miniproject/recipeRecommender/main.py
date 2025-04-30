import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
import os

# Create main window
root = tk.Tk()
root.title("The Veg App")
root.geometry("800x600")  # Adjusted height for better layout
root.configure(bg="#FFFFFF")

# Load and display logo
logo_image = Image.open(r"C:\Users\Sanjita\Desktop\chaggpt\image.png")  # Update with your logo path
logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(root, image=logo_photo, bg="#FFFFFF")
logo_label.place(x=20, y=20)

# Title and subtitle
title_label = tk.Label(root, text="THE VEG APP", font=("Times New Roman", 24, "bold"), bg="#FFFFFF")
title_label.place(x=140, y=30)

subtitle_label = tk.Label(root, text="Your All-Time Recipe Generator", font=("Arial", 12), bg="#FFFFFF")
subtitle_label.place(x=140, y=70)

# Search bar
search_entry = ttk.Entry(root, width=40)
search_entry.place(x=140, y=100)

# Text entry fields (For ingredients)
categories = [("Ingredient 1", "#FFEB99"), ("Ingredient 2", "#FFCCCB"), ("Ingredient 3", "#B3E5FC")]
entries = {}

for i, (category, color) in enumerate(categories):
    frame = tk.Frame(root, bg=color, width=160, height=100)
    frame.place(x=120 + (i * 180), y=150)

    label = tk.Label(frame, text=category, font=("Arial", 10, "bold"), bg=color)
    label.pack(pady=5)

    entry = tk.Entry(frame, font=("Arial", 12), width=18, bg="white", justify="center")
    entry.pack(pady=5, padx=10)
    entries[category] = entry

# Generate Button (Placed below ingredient boxes)
generate_btn = tk.Button(root, text="Generate Recipe", command=lambda: generate_recipe(), font=("Arial", 12), bg="#4CAF50", fg="white")
generate_btn.place(x=320, y=270)

# Output Box (Moved slightly higher)
output_box = tk.Text(root, height=4, width=60, state="disabled", bg="#F0F0F0", font=("Arial", 12))
output_box.place(x=120, y=310)

# Image Label (Lowered to prevent overlap)
image_label = tk.Label(root, bg="#FFFFFF")
image_label.place(x=270, y=400, width=250, height=200)

# Database Connection
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="recipe_db",
            port=3307
        )
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            ingredient1 VARCHAR(255),
                            ingredient2 VARCHAR(255),
                            ingredient3 VARCHAR(255),
                            recipe TEXT,
                            image_path VARCHAR(255))''')
        conn.commit()
        conn.close()
        print("✅ Connected to MySQL successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("❌ Database Error", f"Error: {err}")

# Function to Fetch Recipe & Image
def generate_recipe():
    ingredient1_text = entries["Ingredient 1"].get().lower()
    ingredient2_text = entries["Ingredient 2"].get().lower()
    ingredient3_text = entries["Ingredient 3"].get().lower()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="recipe_db",
            port=3307
        )
        cursor = conn.cursor()

        cursor.execute('''SELECT recipe, image_path FROM recipes WHERE 
                          (ingredient1 = %s OR ingredient2 = %s OR ingredient3 = %s) AND
                          (ingredient1 = %s OR ingredient2 = %s OR ingredient3 = %s) AND
                          (ingredient1 = %s OR ingredient2 = %s OR ingredient3 = %s)''',
                       (ingredient1_text, ingredient1_text, ingredient1_text,
                        ingredient2_text, ingredient2_text, ingredient2_text,
                        ingredient3_text, ingredient3_text, ingredient3_text))

        result = cursor.fetchone()
        conn.close()

        if result:
            output_text = f"✅ Recipe:\n{result[0]}"
            image_path = result[1]

            # Debugging: Print image path to check if it's correct
            print("Trying to load image:", image_path)  

            if image_path and os.path.exists(image_path):  # Check if the image file exists
                img = Image.open(image_path)
                img = img.resize((250, 200), Image.Resampling.LANCZOS)  # Adjusted size
                img_photo = ImageTk.PhotoImage(img)
                image_label.config(image=img_photo)
                image_label.image = img_photo
            else:
                image_label.config(image="", text="❌ Image Not Found", font=("Arial", 10))
                print("❌ Image not found at:", image_path)  # Print error message

        else:
            output_text = "❌ No matching recipe found! Try different ingredients."
            image_label.config(image="", text="")

        output_box.config(state="normal")
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, output_text)
        output_box.config(state="disabled")

    except mysql.connector.Error as err:
        messagebox.showerror("❌ Database Error", f"Error: {err}")

# Initialize database
connect_db()

root.mainloop()
