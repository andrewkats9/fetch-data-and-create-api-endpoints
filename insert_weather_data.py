from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def insert_data(data):

    Base = declarative_base()

    class Forecast(Base):
        __tablename__ = 'forecasts'
        id = Column(Integer, primary_key=True)
        location = Column(String)
        time = Column(DateTime)
        temperature_c = Column(Float)

    engine = create_engine('sqlite:///weather.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    forecast_data = []

    for location, records in data.items():
        for row in records:
            date_obj = row['time']

            forecast_data.append({
                'id': None,
                'location': location,
                'time': date_obj,
                'temperature_c': float(row['temperature_c'])
            })

    for data in forecast_data:
        new_forecast = Forecast(**data)
        session.add(new_forecast)
    
    session.commit()
    
    if len(forecast_data) > 0:
        print('LOG: data uploaded to the db')