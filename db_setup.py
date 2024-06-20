from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

def setup_database():

    Base = declarative_base()

    class Forecast(Base):
        __tablename__ = 'forecasts'
        id = Column(Integer, primary_key=True)
        location = Column(String)
        time = Column(DateTime)
        temperature_c = Column(Float)

    engine = create_engine('sqlite:///weather.db')
    
    # Drop existing tables if they exist
    Base.metadata.drop_all(engine)
    
    # Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print('LOG: db_setup done')
