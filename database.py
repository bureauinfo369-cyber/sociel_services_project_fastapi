from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import os
import sys
import urllib.parse

def load_config(filename):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(base_path, filename)
    with open(config_path, 'r') as file:
        return json.load(file)

def get_database_url():
    config = load_config('config.json')

    username = urllib.parse.quote_plus(config['username'])
    password = urllib.parse.quote_plus(config['password'])
    server = config['server']
    database = config['database']
    port = config.get('port', 1433)

    # Form the connection URL with SSL and timeout parameters
    # TrustServerCertificate=yes bypasses certificate validation
    # Encrypt=no disables encryption (use for development/trusted networks)
    return (f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}"
            f"?driver=ODBC+Driver+17+for+SQL+Server"
            f"&TrustServerCertificate=yes"
            f"&Encrypt=yes"
            f"&timeout=30")

engine = create_engine(
    get_database_url(), 
    connect_args={
        "encoding": "utf-8",
    },
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if __name__ == "__main__":
    print(get_database_url())