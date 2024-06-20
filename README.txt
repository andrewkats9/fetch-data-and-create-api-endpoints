# Data Engineering Project - Andreas Katsaros

## Prerequisites
### Ensure you have the following installed:
- Python 3.10.11

### Open config.json file and insert your "User" and "Password" from https://www.meteomatics.com/en/weather-api/ in order to access the API

## Installation:
### 1) Open a command line (cmd) and go to the repository:
cd ./data-engineering-project-andreas-katsaros

### 2) Create a virtual environment:
python3 -m venv .venv

### 3) Activate the virtual environment:
----For Unix or MacOS:
source .venv/bin/activate
----For Windows:
.\.venv\Scripts\activate

### 4) Install the dependencies:
#### Importand note: The requirements.txt file was created on a Windows PC, and some dependencies might differ on a Mac. Please use the appropriate requirements file for your operating system to avoid compatibility issues.
pip install -r requirements.txt

## Running the application:
python3 app.py

## Visit the local host http://127.0.0.1:8080/ in your browser to check the API's endpoints







## Project Description

Background
For this exercise, we will use the https://www.meteomatics.com/en/weather-api/API, which is an open API that provides weather forecasting information. Look at the endpoints location search for locations and location day for forecasts for a particular day for that location.

Task
- Create a program using your preferred language/tool to get the forecasts for any 3 locations and for a period of 7 days.
- Store the data in a relational database of your choosing (MySQL, MS SQL, SQLite, etc.) with the appropriate schema.
- Create an API that uses the database data and provides endpoints for the following:
List locations
List the latest forecast for each location for every day
List the average the_temp of the last 3 forecasts for each location for every day
Get the top n locations based on each available metric where n is a parameter given to the API call.






## Next Steps:
Ideally deploy the solution to a cloud service (AWS, Azure, GCP, etc.)
