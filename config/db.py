from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

#linea de conexion
engine =create_engine("mysql+pymysql://daniela:123@localhost:3306/storedb")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
meta = MetaData()
conn = engine.connect()
