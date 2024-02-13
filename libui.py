import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk 

import customtkinter
import CTkTable 

import pandas as pd 
from sklearn.model_selection import train_test_split
import classification as cls_
import regression

file_path = ''
df_columns = []

def upload_button_click():
    global file_path
    global df_columns

    file_path = filedialog.askopenfilename(title='Select a CSV file !!!')

    if file_path:
        if file_path.split('.')[-1] != 'csv':
            messagebox.showinfo(title='File type error', message="Please select a CSV file")
            return

        df_columns = list(pd.read_csv(file_path).columns)
        target_combobox.configure(values=df_columns)
    else:
        messagebox.showinfo(title='Not found error', message="No file selected")



models_output_list = []
def train_button_click(selected_model):
    global models_output_list
    target_col = target_combobox.get()
    if selected_model == 'Classification':
        print(target_col)
        df = pd.read_csv(file_path)
        X = df.drop(columns=[target_col]).values
        y = df[target_col]

        y = y.map({'Onaylandı': 1, 'Reddedildi': 0})

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=.2, random_state=42
        )       

        models_output_list = cls_.classification_models(X_train, X_test, y_train, y_test)[0]

        show_model_output(models_output_list)

    elif selected_model == 'Regression':
        print(selected_model)

    else:
        messagebox.showinfo(title='Not found error', message="Model type not selected")

    return None

def show_model_output(output_df):
    value = [list(models_output_list.columns)]

    for row in models_output_list.values:
        value.append(list(row))

    table_container = customtkinter.CTkFrame(root, corner_radius=15)
    table_container.place(relx=0.3, rely=0.05, relwidth=0.68, relheight=0.9)

    table = CTkTable.CTkTable(
        master=table_container, row=len(output_df) + 1, column=len(output_df.columns), 
        values=value, header_color="#204261")
    table.pack(expand=True, fill="both", padx=20, pady=20)

# def change_theme():
#     customtkinter.set_appearance_mode("light")


def on_clear_click():
    file_path = ''
    target_combobox.configure(values=[''])
    combobox.configure(values=[''])

def on_close_click():
    root.destroy()

def library_ui():
    global label
    global root
    global model_type
    global colour1
    global left_container
    global target_combobox
    global output_col_var
    global combobox

    # colour1 = '#292929' # Background color
    colour1 = '#161616'
    colour2 = '#05d7ff' # Default button background color
    colour3 = '#246C71' # Button background color when clicked
    colour4 = 'black' # Text color

    root = customtkinter.CTk()

    root.title("Machine Learnings Library")
    root.resizable(True, True)
    root.geometry("1400x600")  # Width x Height
    root.configure(background=colour1)

    left_container = customtkinter.CTkFrame(root, corner_radius=15)
    left_container.place(relx=0.025, rely=0.05, relwidth=0.25, relheight=0.9)

    # label = tk.Label(left_container, text="Add a CSV file for models")
    # label.pack(pady=10)

    upload_button = tk.Button(
        left_container,
        text='Upload .csv',
        command=upload_button_click,
        background=colour2, # Background color when not hovered
        foreground=colour4, # Text color
        activebackground=colour3, # Background color when hovered/clicked
        activeforeground=colour4, # Text color when hovered/clicked
        highlightthickness=2, # Thickness of the highlight border
        highlightbackground=colour2, # Highlight border color2
        highlightcolor='WHITE', # Highlight color
        width=9,
        height=1,
        border=0,
        cursor='hand1',
        font=('Arial', 16, 'bold')
    )
    upload_button.pack(pady=10)

    output_col_var = customtkinter.StringVar(value="Target Column")
    target_combobox = customtkinter.CTkComboBox(
        master=left_container,
        width=170,
        variable=output_col_var,
        values=['']
    )
    target_combobox.pack(padx=20, pady=10)

    model_type_var = customtkinter.StringVar(value="Machine Learning Type")

    combobox = customtkinter.CTkComboBox(
        master=left_container,
        width=170,     
        values=['Classification', 'Regression'],
        variable=model_type_var
    )
    combobox.pack(padx=20, pady=10)

    train_button = tk.Button(
        left_container,
        text='Train Models',
        command=lambda : train_button_click(combobox.get()),
        background=colour2, # Background color when not hovered
        foreground=colour4, # Text color
        activebackground=colour3, # Background color when hovered/clicked
        activeforeground=colour4, # Text color when hovered/clicked
        highlightthickness=2, # Thickness of the highlight border
        highlightbackground=colour2, # Highlight border color
        highlightcolor='WHITE', # Highlight color
        width=10,
        height=1,
        border=0,
        cursor='hand1',
        font=('Arial', 16, 'bold')
    )
    train_button.pack(pady=10)


    clear_button = tk.Button(
        left_container,
        text='Clear',
        command=on_clear_click,
        background=colour3,
        foreground=colour2,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='WHITE',
        width=8,
        height=1,
        border=0,
        cursor='hand1',
        font=('Arial', 16, 'bold')
    )
    clear_button.pack(pady=50)


    close_button = tk.Button(
        left_container,
        text='Close',
        command=on_close_click,
        background='#a4072c', # gozuken renk
        foreground='white',
        activebackground='#94042b', # tiklayinca 
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='WHITE',
        width=8,
        height=1,
        border=0,
        cursor='hand1',
        font=('Arial', 16, 'bold')
    )
    close_button.pack(side='bottom', pady=50)

    root.mainloop()
    
    return file_path

library_ui()