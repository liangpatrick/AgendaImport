# Utility class to make connecting and initializing tables simpler

# Constant Variables
MAIN ="main"
SUBSSESSION = "subsession"
SPEAKER = "speaker"

MAIN_TABLE_SCHEMA =    {
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

SUBSSESSION_TABLE_SCHEMA = {
        "subsession_id": "INTEGER PRIMARY KEY",
        "session_id": "REFERENCES main (session_id)"
    }

SPEAKER_TABLE_SCHEMA = {
        "speaker": "VARCHAR(16) NOT NULL",
        "session_id": "REFERENCES main (session_id)"
    }   