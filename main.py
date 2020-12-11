import pandas as pd
import numpy as np
import cx_Oracle
import os
import config
from pprint import pprint

from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)

# CSV to Dataframe
print('Reading csv-file 1...')
df0 = pd.read_csv("data.csv",sep=';')
print('Reading csv-file 2...')
df1 = pd.read_csv("authentication.csv",sep=';')
print('Сonverting data to DataFrame...')
mapped=df0[df0['GA'].isin(df1['GA'])]
mapped = mapped.replace(np.nan, '', regex=True)

# Connect to Oracle

LOCATION_ORACLE = r"C:\Users\Влад\Downloads\instantclient_19_9"
os.environ["PATH"] = LOCATION_ORACLE + ";" + os.environ["PATH"]
conn = cx_Oracle.connect(
    config.user, 
    config.password, 
    config.dsn, 
    encoding=config.encoding)
curs = conn.cursor()

# Export Dataframe to Oracle 
print('Exporting data to Oracle DB...')
for item in mapped.values:
 curs.execute(
    "INSERT INTO DATA (GA, GB, G1, G2, G3, G4, G5, G6, G7, G8, G9, G10) VALUES (:GA, :GB, :G1, :G2, :G3, :G4, :G5, :G6, :G7, :G8, :G9, :G10)",
      GA=item[0], GB=item[1], G1=item[2], G2=item[3], G3=item[4], G4=item[5], G5=item[6], G6=item[7], G7=item[8], G8=item[9], G9=item[10], G10=item[11]
      )

conn.commit()
print('Export completed successfully!!!')
conn.close()

