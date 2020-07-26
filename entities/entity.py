from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = 'sql12.freemysqlhosting.net:3306'
db_type = 'mysql'
db_connector = 'pymysql'
db_name = 'sql12356255'
db_user = 'sql12356255'
db_password = 'pqMknJ3YT7'
db_server ='sql12.freemysqlhosting.net'
sqlalchemy_dburl = f'{db_type}+{db_connector}://{db_user}:{db_password}@{db_server}/{db_name}'
engine = create_engine(sqlalchemy_dburl)
Session = sessionmaker(bind=engine)

Base = declarative_base() 


class Entity():
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

