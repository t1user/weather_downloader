from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Weather, Base, Forecast, Item


class Datareader:
    """
    Create database connection, open db and make it available.
    """
    
    engine = create_engine('sqlite:///data.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

"""
NOT IN USE
class Actual(Datareader):

    def __init__(self):
        self.data = self.session.query(Weather)

    def list_cities(self):
        return self.session.query(Weather.city).distinct()

    
    def actual(self, city):
        return self.data.filter(Weather.city == city)


class Diff(Datareader):
    pass
"""
