#!whova/bin/python3
from db_table import db_table
import sys
import xlrd
import schemas

# Load the Excel file using xlrd
if len(sys.argv) != 2:
    raise Exception(
        "Sorry, incorrect number of commandline arguments: " + str(len(sys.argv))+" .Please try again with 2 arguments(if an argument is multiple words, wrap it in quotations so it\'s considered one argument like this:\"Room 201\")")
file_path = sys.argv[1]
agenda = xlrd.open_workbook(file_path)
agenda_sheet = agenda.sheet_by_index(0)

# Initializing tables for SQLite DB
main_table = db_table(schemas.MAIN, schemas.MAIN_TABLE_SCHEMA)

subsession_table = db_table(schemas.SUBSSESSION, schemas.SUBSSESSION_TABLE_SCHEMA)

speaker_table = db_table(schemas.SPEAKER, schemas.SPEAKER_TABLE_SCHEMA)

parent_session_id = 0
# Iterate through rows and insert into the SQLite table
for row_idx in range(15, agenda_sheet.nrows): 
    row = agenda_sheet.row_values(row_idx)
    
    # Formatting and compiling values
    item = {
        "session_id": row_idx - 14,
        "date": str(row[0]).replace("'", "''"), # Escaping apostrophes
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
                "speaker": speaker,
                "session_id": item["session_id"]
            })

# Close the SQLite connections
main_table.close()
subsession_table.close()
speaker_table.close()
