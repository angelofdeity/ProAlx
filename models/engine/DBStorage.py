from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Cohort

# Replace 'your_username', 'your_password', 'your_host', and 'your_database' with your MySQL credentials
DATABASE_URI = 'mysql+mysqlconnector://your_username:your_password@your_host/your_database'

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Create the database tables if they do not exist
User.metadata.create_all(engine)
Cohort.metadata.create_all(engine)
