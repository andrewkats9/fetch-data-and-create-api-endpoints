from fetch_data import get_data
from db_setup import setup_database
from insert_weather_data import insert_data
import uvicorn
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import date, timedelta, datetime

import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.sql import text
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func, desc, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

import warnings
warnings.filterwarnings("ignore")



def main():
    setup_database()
    weather_data = get_data()
    insert_data(weather_data)

    Base = declarative_base()

    class Forecast(Base):
        __tablename__ = 'forecasts'
        id = Column(Integer, primary_key=True)
        location = Column(String)
        time = Column(DateTime)
        temperature_c = Column(Float)

    engine = create_engine('sqlite:///weather.db')
    Base.metadata.bind = engine
    SessionLocal = sessionmaker(bind=engine)

    app = FastAPI()

    
    
    @app.get("/")
    def first_view():
        session = SessionLocal()
        try:
            message = '''This is my Margera weather app project.<br>
    It shows the hourly temperature forecast in 3 different cities.<br>
    1) Click on the <a href="/locations">http://127.0.0.1:8080/locations</a> to see the 3 locations.<br>
    2) Click on the <a href="/average-temperatures">http://127.0.0.1:8080/average-temperatures</a> to see the average temperature forecast (in C) for each city in the next 7 days.<br>
    3) Click on the <a href="/last-three-hours-daily-average-temp">http://127.0.0.1:8080/last-three-hours-daily-average-temp</a> to see the average temperature forecast (in C) of the last 3 hours of the day for each city in the next 7 days.<br>
    4) Click on the <a href="/top-n-locations/3">http://127.0.0.1:8080/top-n-locations/3</a> to see the temperature forecast (in C) for the top 3 locations in the next 7 days. You can also change the number at the end of the url to see 1 or 2 locations.<br>'''
    
            return HTMLResponse(content=message, media_type='text/html')
        finally:
            session.close()




    class AverageTemperature(BaseModel):
        date: str
        avg_temp: float

    class LocationTemperatures(BaseModel):
        location: str
        temperatures: List[AverageTemperature]

    class AverageTemperaturesResponse(BaseModel):
        locations: List[LocationTemperatures]
    
    class Locations(BaseModel):
        locations: List[LocationTemperatures]
    


    @app.get("/locations", response_model=List[str])
    def list_locations():
        session = SessionLocal()
        try:
            locations = session.query(Forecast.location).distinct().all()
            return [loc[0] for loc in locations]
        finally:
            session.close()






    @app.get("/average-temperatures", response_model=AverageTemperaturesResponse)
    def get_average_temperatures():
        session = SessionLocal()
        try:
            # SQL query to calculate daily average temperatures for each location
            sql_query = """
            SELECT location, DATE(time) as date, AVG(temperature_c) as avg_temp
            FROM forecasts
            GROUP BY location, DATE(time);
            """
            result = session.execute(text(sql_query)).fetchall()

            # Organize the result into the desired format
            avg_temps = {}
            for row in result:
                location, date_str, avg_temp = row
                if location not in avg_temps:
                    avg_temps[location] = []
                avg_temps[location].append({"date": date_str, "avg_temp": round(avg_temp, 2)})

            # Convert to the model structure
            formatted_result = {
                "locations": [
                    LocationTemperatures(location=loc, temperatures=temp_list)
                    for loc, temp_list in avg_temps.items()
                ]
            }

            return formatted_result
        finally:
            session.close()







    @app.get("/last-three-hours-daily-average-temp", response_model=AverageTemperaturesResponse)
    def get_average_temperatures_last_three_hours():
        session = SessionLocal()
        try:
            cutoff_time = datetime.now() - timedelta(hours=3)

            sql_query = f"""
                WITH RankedForecasts AS (
                    SELECT 
                        location,
                        DATE(time) AS date,
                        temperature_c,
                        ROW_NUMBER() OVER (PARTITION BY location, DATE(time) ORDER BY time DESC) AS rn
                    FROM forecasts
                    WHERE time >= DATE('now', '-1 day')
                ),
                LastThreeRecords AS (
                    SELECT 
                        location, 
                        date, 
                        AVG(temperature_c) AS avg_temp
                    FROM RankedForecasts
                    WHERE rn <= 3
                    GROUP BY location, date
                )
                SELECT * FROM LastThreeRecords;
            """

            result = session.execute(text(sql_query)).fetchall()

            # Organize the result into the desired format
            avg_temps = {}
            for row in result:
                location, date_str, avg_temp = row
                if location not in avg_temps:
                    avg_temps[location] = []
                avg_temps[location].append(AverageTemperature(date=date_str, avg_temp=round(avg_temp, 2)))

            # Convert to the model structure
            formatted_result = {
                "locations": [
                    LocationTemperatures(location=loc, temperatures=temp_list)
                    for loc, temp_list in avg_temps.items()
                ]
            }

            return formatted_result
        finally:
            session.close()





    @app.get("/top-n-locations/{n}", response_model=Locations)
    def get_top_n_locations(n: int):
        session = SessionLocal()
        try:
            cutoff_time = datetime.now() - timedelta(hours=3)
            
            # SQL query to get the top n locations based on average temperature
            sql_query = f"""
            WITH RankedLocations AS (
                SELECT 
                    location,
                    AVG(temperature_c) AS avg_temp
                FROM forecasts
                WHERE time >= DATE('now', '-1 day')
                GROUP BY location
                ORDER BY avg_temp DESC
                LIMIT {n}
            )
            SELECT * FROM RankedLocations;
            """
            
            result = session.execute(sa.text(sql_query)).fetchall()
            
            # Organize the result into the desired format
            locations_data = []
            for row in result:
                location, avg_temp = row
                temperatures = []  # Fetch or calculate the temperatures for this location here
                locations_data.append(LocationTemperatures(location=location, temperatures=temperatures))
            
            return Locations(locations=locations_data)
        finally:
            session.close()






    
    @app.get("/favicon.ico", include_in_schema=False)
    def favicon():
        return FileResponse("static/favicon.ico")
    
    uvicorn.run(app, host="127.0.0.1", port=8080)





if __name__ == "__main__":
    main()
