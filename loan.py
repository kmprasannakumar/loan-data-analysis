import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load Dataset with Error Handling
file_path = r"C:\Users\HP\Desktop\Loan Data Analysis & Visualization\loan_dataset_5000.csv"
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    messagebox.showerror("Error", "File not found! Check the path.")
    exit()
except pd.errors.EmptyDataError:
    messagebox.showerror("Error", "The file is empty.")
    exit()
except pd.errors.ParserError:
    messagebox.showerror("Error", "Invalid file format.")
    exit()

# Data Preprocessing
df['Default'] = df['Default'].map({'Yes': 1, 'No': 0})
if 'Gender' in df.columns:
    df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})
if 'Education' in df.columns:
    df['Education'] = df['Education'].astype('category').cat.codes

# Handle Missing Values
df.fillna(df.median(numeric_only=True), inplace=True)

# Set Visualization Style
sns.set(style='whitegrid')

# Graphs List
def create_graphs():
    graphs = []

    # 1. Income vs Loan Amount
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=df['Income'], y=df['Loan_Amount'], hue=df['Default'], alpha=0.6, ax=ax)
    ax.set_title('Income vs Loan Amount')
    graphs.append(fig)

    # 2. Credit Score Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df['Credit_Score'], bins=30, kde=True, ax=ax)
    ax.set_title('Credit Score Distribution')
    graphs.append(fig)

    # 3. Loan Default vs Loan Amount
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x=df['Default'], y=df['Loan_Amount'], ax=ax)
    ax.set_title('Loan Amount vs Default Status')
    graphs.append(fig)

    # 4. Age vs Loan Default Trend
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df[df['Default'] == 0]['Age'], bins=30, color='green', label='No Default', kde=True, ax=ax)
    sns.histplot(df[df['Default'] == 1]['Age'], bins=30, color='red', label='Default', kde=True, ax=ax)
    ax.legend()
    ax.set_title('Age Distribution of Loan Defaults')
    graphs.append(fig)

    # 5. Loan Default by Gender
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(x='Gender', hue='Default', data=df, ax=ax)
    ax.set_title('Loan Default by Gender')
    graphs.append(fig)

    # 6. Correlation Heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    corr_matrix = df.select_dtypes(include=[np.number]).corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    ax.set_title('Correlation Heatmap')
    graphs.append(fig)

    return graphs

# GUI Setup
def show_graph(index):
    global graph_canvas
    graph_canvas.get_tk_widget().destroy()
    fig = graph_cache[index]
    graph_canvas = FigureCanvasTkAgg(fig, master=frame)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack()

def next_graph():
    global graph_index
    if graph_index < len(graph_cache) - 1:
        graph_index += 1
        show_graph(graph_index)

def prev_graph():
    global graph_index
    if graph_index > 0:
        graph_index -= 1
        show_graph(graph_index)

def update_graph(event):
    selected_index = graph_dropdown.current()
    show_graph(selected_index)

def save_graph():
    fig = graph_cache[graph_index]
    fig.savefig(f"graph_{graph_index}.png", dpi=300)
    messagebox.showinfo("Success", f"Graph {graph_index} saved as an image!")

def close_app():
    root.destroy()

# Initialize GUI
root = tk.Tk()
root.title("Borrow Trends Analysis")
root.geometry("900x700")

# Title Label
title_label = ttk.Label(root, text="Borrow Trends Analysis Project", font=("Arial", 20))
title_label.pack(pady=10)

# Frame for Graphs
frame = ttk.Frame(root)
frame.pack()

# Generate Graphs
graph_cache = create_graphs()
graph_index = 0
graph_canvas = FigureCanvasTkAgg(graph_cache[graph_index], master=frame)
graph_canvas.draw()
graph_canvas.get_tk_widget().pack()

# Dropdown for Graph Selection
graph_dropdown = ttk.Combobox(root, values=[
    "Income vs Loan Amount",
    "Credit Score Distribution",
    "Loan Amount vs Default",
    "Age Distribution of Loan Defaults",
    "Loan Default by Gender",
    "Correlation Heatmap"
])
graph_dropdown.pack()
graph_dropdown.bind("<<ComboboxSelected>>", update_graph)

# Button Frame
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=20)

prev_btn = ttk.Button(btn_frame, text="Previous", command=prev_graph)
prev_btn.grid(row=0, column=0, padx=10)

next_btn = ttk.Button(btn_frame, text="Next", command=next_graph)
next_btn.grid(row=0, column=1, padx=10)

save_btn = ttk.Button(btn_frame, text="Save Graph", command=save_graph)
save_btn.grid(row=0, column=2, padx=10)

close_btn = ttk.Button(root, text="Close", command=close_app)
close_btn.pack(pady=10)

root.mainloop()

# Save Processed Data
df.to_csv("processed_loan_data.csv", index=False)
