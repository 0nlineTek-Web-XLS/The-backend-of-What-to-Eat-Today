from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/demo"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://1QW6E7P7YUNRMVA5$:suyrbmymqs@0nlinetek-eat-server.mysql.database.azure.com:3306/0nlinetek-eat-database"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
