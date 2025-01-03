from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATABASE_URL= 'postgresql://todoappdatabase_nc0h_user:fdY8TcaOY4dsMzS7sac5Qlklfg8mL95a@dpg-ctrmpm3tq21c738ui8ug-a.singapore-postgres.render.com/todoappdatabase_nc0h'
# SQLALCHEMY_DATABASE_URL= 'postgresql://postgres:test1234!@localhost/TodoApplicationDatabase'
# SQLALCHEMY_DATABASE_URL= 'mysql+pymysql://root:test1234@127.0.0.1:3306/todoapplicationdatabase'
engine= create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base= declarative_base()