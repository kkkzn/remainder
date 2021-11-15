import os

import pandas as pd
from sqlalchemy import create_engine
from tz_table import tz_table


table = tz_table()

df = pd.DataFrame(table)

engine = create_engine(os.environ.get('DATABASE_URL'))

df.to_sql('timezone', con=engine, if_exists='append', index=False)

print(engine.execute('SELECT * FROM timezone').fetchall())
