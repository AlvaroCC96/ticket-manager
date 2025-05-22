from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Date, MetaData, Table
)
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./boletas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

boletas = Table(
    "boletas", metadata,
    Column("id", Integer, primary_key=True),
    Column("empresa", String),
    Column("servicio", String),
    Column("monto", Float),
    Column("fecha", Date),
    Column("archivo", String)
)

metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
