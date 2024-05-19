from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

#linea de conexion
engine =create_engine("mysql+pymysql://user:pass@localhost:3306/name_db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
meta = MetaData()
conn = engine.connect()
