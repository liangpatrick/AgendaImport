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
iniitial_results = []
if "speaker" in columns:
    speakers = speaker_table.select([], where_param)
    new_where_param = {}
    for row in speakers:
        if "session_id" not in new_where_param:
            new_where_param["session_id"] = []
        new_where_param["session_id"].append(row["session_id"])
    iniitial_results = main_table.select([], new_where_param, "OR")
else:
    iniitial_results = main_table.select([], where_param)


main_table.close()
subsession_table.close()
speaker_table.close()
