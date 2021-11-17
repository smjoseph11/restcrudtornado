from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from widgets.models import Base, Widget

eng = create_engine('sqlite:///widgets.db')

Base.metadata.bind = eng
Base.metadata.create_all() 

Session = sessionmaker(bind=eng) 
