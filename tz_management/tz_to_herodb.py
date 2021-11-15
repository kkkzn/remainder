import os

import pandas as pd
from sqlalchemy import create_engine
from tz_table import tz_table


table = tz_table()

df = pd.DataFrame(table)

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
if SQLALCHEMY_DATABASE_URI is not None:
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URI)

df.to_sql('timezone', con=engine, if_exists='append', index=False)

print(engine.execute('SELECT * FROM timezone').fetchall())
