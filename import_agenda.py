from db_table import db_table
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
        "speaker": "TEXT NOT NULL"
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

parent_session_id = 0
# Iterate through rows and insert into the SQLite table
for row_idx in range(15, agenda_sheet.nrows): 
    row = agenda_sheet.row_values(row_idx)
    item = {
        "session_id": row_idx - 14,
        "date": str(row[0]).replace("'", "''"),
        "time_start": str(row[1]).replace("'", "''"),
        "time_end": str(row[2]).replace("'", "''"),
        "session_type": str(row[3]).replace("'", "''"),
        "title": str(row[4]).replace("'", "''"),
        "location": str(row[5]).replace("'", "''"),
        "description": str(row[6]).replace("'", "''"),
        "speaker": str(row[7]).replace("'", "''")
    }

    main_table.insert(item)
    if item["session_type"] == "Sub":
        subsession_table.insert({
            "subsession_id": item["session_id"],
            "session_id": parent_session_id
        })
    else:
        parent_session_id = item["session_id"]

    # Parsing speakers into Speaker table
    if len(item["speaker"]) > 0:
        speakers = item["speaker"].split(';')
        for speaker in speakers:
            speaker_table.insert({
                "speaker_name": speaker,
                "session_id": item["session_id"]
            })

# Close the SQLite connections
main_table.close()
subsession_table.close()
speaker_table.close()
