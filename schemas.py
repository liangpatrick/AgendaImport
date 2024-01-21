MAIN ="main"
SUBSSESSION = "subsession"
SPEAKER = "speaker"

def main_table_schema():
    return {
        "session_id": "INTEGER PRIMARY KEY", 
        "date": "VARCHAR(16) NOT NULL", 
        "time_start": "VARCHAR(16) NOT NULL",
        "time_end": "VARCHAR(16) NOT NULL",
        "session_type": "VARCHAR(16) NOT NULL",
        "title": "TEXT NOT NULL",
        "location": "TEXT NOT NULL",
        "description": "TEXT NOT NULL",
        "speaker": "TEXT NOT NULL"
    }

def subsession_table_schema():
    return {
        "subsession_id": "INTEGER PRIMARY KEY",
        "session_id": "INTEGER",
        "FOREIGN KEY(session_id)": "REFERENCES main (session_id)"
    }

def speaker_table_schema():
    return {
        "speaker_name": "VARCHAR(16) NOT NULL",
        "session_id": "INTEGER",
        "FOREIGN KEY(session_id)": "REFERENCES main (session_id)"
    }   