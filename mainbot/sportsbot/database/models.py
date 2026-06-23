from sqlalchemy import *

from database.db import engine

metadata = MetaData()

games = Table(
    "games",
    metadata,

    Column("id", Integer, primary_key=True),

    Column("home_team", String),
    Column("away_team", String),

    Column("home_score", Integer),
    Column("away_score", Integer),

    Column("date", String)
)

metadata.create_all(engine)