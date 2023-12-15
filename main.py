import os
import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def find_csv_files(start_dir: str):
    """
    Recursively find all CSV files in a directory and its subdirectories.

    Args:
        start_dir (str): The directory to start searching from.

    Returns:
        list: A list of CSV file paths.
    """
    csv_files = []

    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))

    return csv_files


def create_database(db_name='Chinese_Cases.db'):
    """
    Function to createa SQLite database.

    Parameters:
    - db_name (str): Name of the SQLite database. Default is 'Chinese_Cases.db'.

    Returns:
    - None
    """
    result_label.config(text='')
    # Parameter validation
    if not os.path.exists(db_name):
        print(f"The database file {db_name} does not exist. Creating...")
        db_connection = sqlite3.connect(db_name)
        db_connection.close()


def adding_CSV(db_name='Chinese_Cases.db', csv_file='', table_name='chinese_cases', delimiter=','):
    """
    This function adds data from a CSV file to a specified table in a SQLite database.

    Parameters:
    - db_name (str): The name of the SQLite database file. Default is 'Chinese_Cases.db'.
    - csv_file (str): The path of the CSV file to be loaded. Default is an empty string, indicating that no file is provided.
    - table_name (str): The name of the table in the database where the data will be added. Default is 'chinese_cases'.
    - delimiter (str): The delimiter used in the CSV file to separate values. Default is ','.

    Returns:
    None
    """
    try:
        # Check if the csv_file path is valid and ends with '.csv'
        if csv_file and csv_file.endswith('.csv'):
            print(f"Loading {csv_file} into the database...")
            try:
                conn = sqlite3.connect(db_name)
                # Read the CSV file, skipping NaN values
                df = pd.read_csv(csv_file, delimiter=delimiter, keep_default_na=False, na_values=[''])
                # Insert new records into the database table
                df.to_sql(table_name, conn, if_exists='append', index=False, index_label='id')
            except Exception as e:
                print(f"Error loading {csv_file}: {e}")

            finally:
                conn.commit()
                conn.close()

        else:
            print("No valid CSV file provided or found.")
    except FileNotFoundError:
        print(f"File {csv_file} was not found.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception error: {e}")
    

def create_index(db_name, table_name):
    conn = sqlite3.connect(db_name)    
    try:
        cursor = conn.cursor()
        # Based on actual requirements
        indexes = ["案件名称", "案号", "法院", "案由"]
        for index in indexes:
            # Trying to delete an existing index
            cursor.execute(f'DROP INDEX IF EXISTS "idx_{table_name}_{index}"')
            # Create a new index
            cursor.execute(f'CREATE INDEX IF NOT EXISTS "idx_{table_name}_{index}" ON "{table_name}" ("{index}")')
        print(f"Indexes created or updated for table {table_name}")
    except sqlite3.Error as e:
        print(f"Error creating or updating indexes: {e}")
    finally:
        conn.commit()
        conn.close()


def query_data(searching_dict, table_name='chinese_cases', fuzzy_search=True):
    """
    Function to query data from a SQLite database.

    Parameters:

    - searching_dict (dict): A dictionary containing search criteria where keys are column names and values are lists of values to search for.

    - table_name (str): Name of the table in the database to query. Default is 'chinese_cases'.

    - fuzzy_search (bool): If True, performs a fuzzy search using 'LIKE'; if False, performs an
    exact match using '='. Default is True.

    Returns:
    - result (pd.DataFrame): A Pandas DataFrame containing the query results.
    """
    # Make a copy of searching_dict to avoid modifying the original dictionary
    searching_dict = dict(searching_dict)

    # Connect to the SQLite database
    db_connection = sqlite3.connect('Chinese_Case.db')

    # Build the criteria string for the SQL query
    criteria = []

    # Build the list of query parameters
    values = []

    for column, column_values in searching_dict.items():
        # Handle fuzzy search and exact match
        if fuzzy_search:
            conditions = [f"{column} LIKE '%{value}%'" for value in column_values]
        else:
            conditions = [f"{column} = '{value}'" for value in column_values]

        criteria.append(f"({' OR '.join(conditions)})")

        # Add the parameters to the values list
        values.extend(column_values)

    # Build the complete SQL query statement
    query = f"SELECT * FROM {table_name} WHERE {' AND '.join(criteria)};"
    print(query)

    # Execute the query and store the result in a Pandas DataFrame
    result = pd.read_sql_query(query, db_connection)

    # Close the database connection
    db_connection.close()

    return result


def get_unique_values(db_name='Chinese_Case.db', table_name='chinese_cases', column_name='案件类型'):
    """
    Function to retrieve unique values from a specific column in a SQLite database table.

    Parameters:
    - db_name (str): Name of the SQLite database. Default is 'Chinese_Case.db'.
    - table_name (str): Name of the table in the database. Default is 'chinese_cases'.
    - column_name (str): Name of the column from which to retrieve unique values. Default is 'case_type'.

    Returns:
    - unique_values (list): A list of unique values from the specified column.
    """
    try:
        # Connect to the database
        db_connection = sqlite3.connect(db_name)

        # Execute SQL query to get unique values
        query = f"SELECT DISTINCT {column_name} FROM {table_name};"
        unique_values = pd.read_sql_query(query, db_connection)[column_name].tolist()

        # Close the database connection
        db_connection.close()

        return unique_values

    except sqlite3.Error as e:
        print("Database error: ", e)
        return None
    except Exception as e:
        print("Exception error: ", e)
        return None


def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        csv_path_var.set(folder_selected)


def start_create_database():
    db_name = db_name_entry.get()
    csv_dir = csv_path_entry.get()
    delimiter = ','

    if language_button.cget("text") == "CN":
        completed_text = 'Database creation completed!'
        error_text = "Creating Error:"
        btn_text_Creating = 'Creating...'
        btn_text_Done = 'Create Database'
        create_status_window_title = 'Creating...Please DO NOT CLOSE'
        error_window_title = 'Error'
        error_window_btn_text = 'Close'
        error_window_path_text = 'Please select the CSV path first.'
    else:
        completed_text = '创建数据库成功!'
        error_text = "创建错误:"
        btn_text_Creating = '创建中...'
        btn_text_Done = '创建数据库'
        create_status_window_title = '创建中...请勿关闭'
        error_window_title = '错误'
        error_window_btn_text = '关闭'
        error_window_path_text = '请先选择CSV路径'

    create_button.configure(text=btn_text_Creating, state='disabled')
    if not csv_dir:
        error_window = tk.Toplevel(window)
        error_window.title(error_window_title)
        error_label = tk.Label(error_window, text=error_window_path_text, padx=20, pady=20)
        error_label.pack()

        def _reset():
            create_button.configure(text=btn_text_Done, state='normal')
            error_window.destroy()

        close_button = tk.Button(error_window, text=error_window_btn_text, command=_reset)
        close_button.pack(pady=10)

        return 0

    try:
        create_database(db_name)
        create_status_window = tk.Toplevel(window, width=600,height=400)
        create_status_window.title(create_status_window_title)
        files = find_csv_files(csv_dir)
        pb = ttk.Progressbar(create_status_window,
                             length=100,
                             maximum=100,
                             mode='determinate',
                             orient="horizontal",
                             )
        pb.pack(pady=10)
        loading_file_text = tk.Label(create_status_window, text="")
        loading_file_text.pack(pady=10)

        for i in range(len(files)):
            file_name = os.path.basename(files[i])
            loading_file_text.config(text=f"Loading {file_name}...")
            table_name = file_name[:4] # 8 if hardware performance is insufficient
            adding_CSV(db_name=db_name, csv_file=files[i], table_name=table_name, delimiter=delimiter)
            create_index(db_name=db_name, table_name=table_name)
            pb['value'] = 100 * (i/len(files))
            create_status_window.update()
        create_status_window.destroy()
        result_label.config(text=completed_text)
        create_button.configure(text=btn_text_Done, state='normal')
    except Exception as e:
        result_label.config(text=f"{error_text}{e}")


def show_about_window():
    # Only create the about_window if it doesn't exist or has been destroyed
    current_language = language_button.cget("text")
    about_window = tk.Toplevel(window, width=300)
    if current_language == "CN":
        about_window.title("About")
        about_text = """The program is primarily designed to adapt to the Chinese case database file (CSV) circulating online as of December 2023.\n
        In most cases, only the folder path needs to be selected, and other settings should remain unchanged.\n
        Author: Li Boyang — Beijing Long'an (Guangzhou) Law Firm"""
    else:
        about_window.title("关于")
        about_text = ("本程序主要适配2023年12月网上流传的中国案例数据库文件（CSV）\n\n"
                      "一般情况下只需要选择文件夹路径即可，其他不需要改变\n\n"
                      "本软件作者：李伯阳 —— 北京市隆安（广州）律师事务所")
    about_label = tk.Label(about_window, text=about_text, padx=20, pady=20, compound='left')
    about_label.pack()


def toggle_language():
    # Function to toggle between English and Chinese
    current_language = language_button.cget("text")

    if current_language == "EN":
        language_button.config(text="CN")
        db_name_label.config(text="Database Name:")
        browse_button.config(text="Select CSV Folder")
        create_button.config(text="Create Database")
        about_button.config(text="About")
        result_label.config(text="")
        csv_path_label.config(text='CSV filepath:')
        window.title('Create Chinese Cases Database')
    else:
        language_button.config(text="EN")
        db_name_label.config(text="数据库名称:")
        browse_button.config(text="选择CSV文件夹")
        create_button.config(text="创建数据库")
        about_button.config(text="关于")
        result_label.config(text="")
        csv_path_label.config(text='CSV 文件路径:')
        window.title("创建案例数据库")


if __name__ == '__main__':
    # Create the main window
    window = tk.Tk()
    window.title("创建案例数据库")

    # Create and set variables for entry fields
    db_name_entry = tk.Entry(window, width=30, textvariable=tk.StringVar(value="Chinese_Cases.db"), justify='center')
    csv_path_var = tk.StringVar(value="inputCSV")
    csv_path_entry = tk.Entry(window, width=30, textvariable=csv_path_var, justify='center')

    # Create and set labels for entry fields
    db_name_label = tk.Label(window, text="数据库名称:")
    csv_path_label = tk.Label(window, text="CSV 文件路径:")

    # Create and set the folder selection button
    browse_button = tk.Button(window, text="选择CSV文件夹", command=browse_folder, width=20)

    # Create and set the create database button
    create_button = tk.Button(window, text="创建数据库", command=start_create_database, width=20)

    # Create a label to display the result
    result_label = tk.Label(window, text="")

    # Create and set the language toggle button
    language_button = tk.Button(window, text="EN", command=toggle_language)

    # Create and set the "About" button
    about_button = tk.Button(window, text="关 于", command=show_about_window)

    # Arrange the widgets in the window
    db_name_label.grid(row=0, column=0, pady=5)
    db_name_entry.grid(row=0, column=1, pady=5)
    csv_path_label.grid(row=2, column=0, pady=5)
    csv_path_entry.grid(row=2, column=1, pady=5)
    browse_button.grid(row=3, column=0, columnspan=2, pady=10)
    create_button.grid(row=4, column=0, columnspan=2, pady=10)
    result_label.grid(row=5, column=0, columnspan=2, pady=10)
    about_button.grid(row=6, column=1, sticky="se", padx=10, pady=10)
    language_button.grid(row=6, column=2, sticky="se", padx=10, pady=10)

    # Start the GUI main loop
    window.mainloop()
