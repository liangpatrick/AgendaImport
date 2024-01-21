from db_table import db_table
import sys
import schemas
# columns = sys.argv[1].split(",")
# values = sys.argv[2].split(",")

# where_param = {}
# for x in range((len(values))):
#     where_param[columns[x]] = values[x]

columns = sys.argv[1]
values = sys.argv[2].replace("," ," ")
where_param = {}
where_param[columns] = str(values)
main_table = db_table(schemas.MAIN, schemas.MAIN_TABLE_SCHEMA)

subsession_table = db_table(schemas.SUBSSESSION, schemas.SUBSSESSION_TABLE_SCHEMA)
speaker_table = db_table(schemas.SPEAKER, schemas.SPEAKER_TABLE_SCHEMA)

# If speaker is being searched, then need to search speaker table first to build new where parameter
sessions = []
if "speaker" in columns:
    speakers = speaker_table.select(["session_id"], where_param)
    new_where_param = {}
    new_where_param["session_id"] = []
    for row in speakers:            
        new_where_param["session_id"].append(row["session_id"])
    sessions = main_table.select([], new_where_param, "OR")
else:
    sessions = main_table.select([], where_param)

# Searching for subsessions
session_ids_where_param = {}
session_ids_where_param["session_id"] = []
for row in sessions:
    session_ids_where_param["session_id"].append(row["session_id"])
subsessions = subsession_table.select(["subsession_id"], session_ids_where_param, "OR")

# If subsessions exist, add to sessions
if len(subsessions) > 0:
    subsession_ids_where_param  = {}
    subsession_ids_where_param["session_id"] = []
    for row in subsessions:
        subsession_ids_where_param["session_id"].append(row["subsession_id"])
    sessions.extend(main_table.select([], subsession_ids_where_param, "OR"))

# Printing sessions
for session in sessions:
    print(session + "\n\n")


main_table.close()
subsession_table.close()
speaker_table.close()
