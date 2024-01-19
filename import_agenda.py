from db_table import db_table
from datetime import datetime
import sys
import xlrd

# Load the Excel file using xlrd
file_path = sys.argv[1]
agenda = xlrd.open_workbook(file_path)
agenda_sheet = agenda.sheet_by_index(0)

# Initializing tables for SQLite DB
main_table = db_table("main", {
        "session_id": "INTEGER PRIMARY KEY", 
        "date": "VARCHAR(16) NOT NULL", 
        "time_start": "VARCHAR(16) NOT NULL",
        "time_end": "VARCHAR(16) NOT NULL",
        "session_type": "VARCHAR(16) NOT NULL",
        "title": "TEXT NOT NULL",
        "location": "TEXT NOT NULL",
        "description": "TEXT NOT NULL",
        "speaker": "TEXT NOT NULL",
        "subsessions": "TEXT NOT NULL"
})

subsession_table = db_table("subsession", {
    "subsession_id": "INTEGER PRIMARY KEY",
    "session_id": "INTEGER",
    "FOREIGN KEY(session_id)": "REFERENCES main (session_id)"
})
speaker_table = db_table("speaker", {
    "speaker_name": "VARCHAR(16) NOT NULL",
    "session_id": "INTEGER",
    "FOREIGN KEY(session_id)": "REFERENCES main (session_id)"
})


main_table.close()
subsession_table.close()
speaker_table.close()
