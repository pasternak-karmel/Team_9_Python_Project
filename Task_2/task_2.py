# import tkinter as tk
# from tkinter import filedialog, messagebox
# import pandas as pd
# import pickle
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
#
# from sklearn.preprocessing import StandardScaler
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import OrdinalEncoder
#
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.ensemble import RandomForestRegressor
# from xgboost import XGBRegressor
#
# from sklearn.metrics import mean_squared_error
# from sklearn import metrics
#
#
# label_encoder = LabelEncoder()
# ordinal_encoder = OrdinalEncoder(categories=[['unfurnished','semi-furnished','furnished']])
# dataframe['mainroad'] = label_encoder.fit_transform(dataframe['mainroad'])
# dataframe['guestroom'] = label_encoder.fit_transform(dataframe['guestroom'])
# dataframe['basement'] = label_encoder.fit_transform(dataframe['basement'])
# dataframe['hotwaterheating'] = label_encoder.fit_transform(dataframe['hotwaterheating'])
# dataframe['airconditioning'] = label_encoder.fit_transform(dataframe['airconditioning'])
# dataframe['prefarea'] = label_encoder.fit_transform(dataframe['prefarea'])
# dataframe['furnishingstatus'] = ordinal_encoder.fit_transform(dataframe[['furnishingstatus']])
#
# dataframe.hist(figsize=(15,10))
#
# def select_file():
#     # Open a file dialog and allow only csv files to be selected
#     file_path = filedialog.askopenfilename(
#         filetypes=[("CSV files", "*.csv")],
#         title="Choose a CSV file"
#     )
#
#     if file_path:
#         try:
#             # Read the CSV file
#             data = pd.read_csv(file_path)
#             # Display the first few rows of the dataframe (for demonstration purposes)
#             print(data.head())
#             messagebox.showinfo("File Loaded", "CSV file loaded successfully!")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to read file\n{e}")
#
#
# # Create the main window
# root = tk.Tk()
# root.title("CSV File Reader")
#
# # Create a button that calls the select_file function
# btn = tk.Button(root, text="Select CSV File", command=select_file)
# btn.pack(pady=20)
#
# # Run the GUI event loop
# root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt


def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="Choose a CSV file"
    )

    if file_path:
        try:
            global data
            data = pd.read_csv(file_path)
            print(data.head())
            messagebox.showinfo("File Loaded", "CSV file loaded successfully!")

            numeric_columns = data.select_dtypes(include='number').columns.tolist()
            column_dropdown['values'] = numeric_columns
            x_column_dropdown['values'] = numeric_columns
            y_column_dropdown['values'] = numeric_columns
            if numeric_columns:
                column_dropdown.current(0)
                x_column_dropdown.current(0)
                if len(numeric_columns) > 1:
                    y_column_dropdown.current(1)
            update_widgets_state('normal')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file\n{e}")


def create_plot():
    if data is None or data.empty:
        messagebox.showwarning("Warning", "No CSV file loaded.")
        return

    plot_type = plot_type_var.get()

    if plot_type == "Histogram":
        create_histogram()
    elif plot_type == "Scatter Plot":
        create_scatter_plot()
    else:
        messagebox.showwarning("Warning", "Please select a plot type.")


def create_histogram():
    selected_column = column_dropdown.get()

    if selected_column:
        try:
            plt.hist(data[selected_column].dropna(), bins=10, edgecolor='black')
            plt.title(f'Histogram of {selected_column}')
            plt.xlabel(selected_column)
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create histogram\n{e}")
    else:
        messagebox.showwarning("Warning", "No column selected.")


def create_scatter_plot():
    x_column = x_column_dropdown.get()
    y_column = y_column_dropdown.get()

    if x_column and y_column:
        try:
            plt.scatter(data[x_column], data[y_column])
            plt.title(f'Scatter Plot of {x_column} vs {y_column}')
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.grid(True)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create scatter plot\n{e}")
    else:
        messagebox.showwarning("Warning", "Please select both X and Y columns.")


def update_widgets_state(state):
    column_dropdown.config(state=state)
    x_column_dropdown.config(state=state)
    y_column_dropdown.config(state=state)
    create_plot_btn.config(state=state)
    hist_radio_btn.config(state=state)
    scatter_radio_btn.config(state=state)


root = tk.Tk()
root.title("CSV Data Plotter")
root.geometry("400x300")
root.resizable(False, False)

style = ttk.Style()
style.configure('TFrame', background='lightblue')
style.configure('TLabel', background='lightblue', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10))
style.configure('TRadiobutton', background='lightblue', font=('Arial', 10))

frame = ttk.Frame(root, padding="10 10 10 10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

data = None

plot_type_var = tk.StringVar(value="Histogram")

hist_radio_btn = ttk.Radiobutton(frame, text="Histogram", variable=plot_type_var, value="Histogram")
scatter_radio_btn = ttk.Radiobutton(frame, text="Scatter Plot", variable=plot_type_var, value="Scatter Plot")
hist_radio_btn.grid(column=0, row=0, sticky=tk.W, pady=5)
scatter_radio_btn.grid(column=1, row=0, sticky=tk.W, pady=5)

select_file_btn = ttk.Button(frame, text="Select CSV File", command=select_file)
select_file_btn.grid(column=0, row=1, columnspan=2, pady=10)

column_dropdown_label = ttk.Label(frame, text="Select Column for Histogram:")
column_dropdown_label.grid(column=0, row=2, sticky=tk.W, pady=5)
column_dropdown = ttk.Combobox(frame, state="readonly")
column_dropdown.grid(column=1, row=2, pady=5)

x_column_dropdown_label = ttk.Label(frame, text="Select X Column for Scatter Plot:")
x_column_dropdown_label.grid(column=0, row=3, sticky=tk.W, pady=5)
x_column_dropdown = ttk.Combobox(frame, state="readonly")
x_column_dropdown.grid(column=1, row=3, pady=5)

y_column_dropdown_label = ttk.Label(frame, text="Select Y Column for Scatter Plot:")
y_column_dropdown_label.grid(column=0, row=4, sticky=tk.W, pady=5)
y_column_dropdown = ttk.Combobox(frame, state="readonly")
y_column_dropdown.grid(column=1, row=4, pady=5)

create_plot_btn = ttk.Button(frame, text="Create Plot", command=create_plot)
create_plot_btn.grid(column=0, row=5, columnspan=2, pady=20)

update_widgets_state('disabled')

root.mainloop()

