from numpy import genfromtxt
from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


def Load_Data(file_name):
    data = genfromtxt(file_name, dtype=(int, "|S100", "|S100", "|S10", float, \
                        float, "|S100", "|S100", float, float), delimiter=',', \
                        skiprows=1, converters={0: lambda s: str(s)})
    return data.tolist()

Base = declarative_base()

class Bus_Stops(Base):

    __tablename__ = 'Bus_Stops'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, nullable=False) 
    stop_id = Column(Integer)
    on_street = Column(String(100))
    cross_street = Column(String(100))
    routes = Column(String(10))
    boardings = Column(Float)
    alightings = Column(Float)
    month_beginning = Column(String(100))
    daytype = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)

if __name__ == "__main__":

    #Create the database
    engine = create_engine('sqlite:///busstops2012.db')
    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        file_name = "cutfile.csv"
        data = Load_Data(file_name) 

        for i in data:
            record = Bus_Stops(**{
                'stop_id' : i[0],
                'on_street' : i[1],
                'cross_street': i[2],
                'routes' : i[3],
                'boardings' : i[4],
                'alightings' : i[5],
                'month_beginning' : i[6],
                'daytype' : i[7],
                'latitude': i[8],
                'longitude': i[9]
            })
            s.add(record) #Add all the records
        s.commit() #Attempt to commit all the records
    except:
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection