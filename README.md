# trading-analyzer
A small trading analyzer dashboard using django , postgres database and angular


### Database setup
    1 Install postgres sql (https://www.postgresql.org/download/)
    2 Create database named 'trading' (CREATE DATABASE demo;)
    3 Create user (CREATE USER test WITH PASSWORD 't!@123';)

###  Install Dependencies & run backend
    1 Setup virtual env
        `
            > pip install virtualenvwrapper-win
            > mkvirtualenv env_name
        `
    2 Install dependencies (pip install -r requirements.txt)
    3 Run the project
      > python manage.py runserver

### Model Migration
    1 python manage.py makemigrations
    2 python manage.py migrate
        # it will create table in your database
        + table 'analyzer'
### Import dummy data (table) analyzer.csv (tmp/)
    >COPY analyzer_analyzer("Date","Open","Close","High","Low","Shares_Traded","Turnover") FROM 'C:\tmp\analyzer.csv' DELIMITER ',' CSV HEADER;

### Import Postman Collection and Check APIs
    tmp/

### Also Clone, Install and Run Trading App from given repo
    https://github.com/uds214125/trading-app

    > npm i
    > ng serve