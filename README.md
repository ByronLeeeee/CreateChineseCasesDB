# Chinese Cases Database Creator

[中文说明](./README_CN.md)

This Python script provides a GUI application to create a SQLite database for Chinese legal cases from CSV files. It includes functionalities such as:

- Recursive search for CSV files in a specified directory.
- Creation of a SQLite database and addition of data from CSV files to corresponding tables.
- Index creation for specific columns to enhance query performance.
- Querying data based on specified criteria.
- Retrieving unique values from a specific column in the database table.

## Requirements

- Python 3.x
- pandas

## Usage

1. Run the script using a Python interpreter.
2. Select a database name and the folder containing the Chinese legal case CSV files.
3. Click the "Create Database" button to initiate the database creation process.
4. The process completion message will be displayed, indicating a successful database creation.

## GUI Instructions

- **Database Name:** Enter the desired name for the SQLite database.
- **CSV File Path:** Enter or browse to the folder containing the Chinese legal case CSV files.
- **Select CSV Folder:** Click to browse and select the CSV file folder.
- **Create Database:** Click to start the database creation process.
- **EN/CN:** Toggle between English and Chinese language.

## Notes

- The script is designed to adapt to Chinese case database files circulating online as of December 2023.
- Selecting the folder path is typically the only required configuration; other settings can remain unchanged.

## License

This script is provided under the [MIT License](LICENSE).
