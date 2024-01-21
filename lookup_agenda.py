from db_table import db_table
import sys
import schemas
columns = sys.argv[1].split(",")
values = sys.argv[2].split(",")


main_table = db_table(schemas.MAIN, schemas.main_table_schema())
subsession_table = db_table(schemas.SUBSSESSION, schemas.subsession_table_schema())
speaker_table = db_table(schemas.SPEAKER, schemas.speaker_table_schema())




main_table.close()
subsession_table.close()
speaker_table.close()
