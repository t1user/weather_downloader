import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    timestamp = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow)
    city = Column(String)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    weather = Column(String)
    weather_detail = Column(String)
    wind_speed = Column(Float)
    wind_deg = Column(Float)
    wind_gust = Column(Float)
    visibility = Column(String)
    clouds = Column(Float)
    dt = Column(DateTime)


class Forecast(Base):
    __tablename__ = 'forecasts'
    id = Column(Integer, primary_key=True)
    timestamp = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow)
    city = Column(String)
    forecasts = relationship('Item', back_populates='forecast')


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    forecast_id = Column(Integer, ForeignKey('forecasts.id'))
    forecast = relationship('Forecast', back_populates='forecasts')
    t = Column(Integer)
    timestamp = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow)
    temperature = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    weather = Column(String)
    weather_detail = Column(String)
    clouds = Column(Float)
    wind_speed = Column(Float)
    wind_deg = Column(Float)
    wind_gust = Column(Float)
    rain = Column(Float)
    dt = Column(DateTime)


engine = create_engine('sqlite:///data.db')

Base.metadata.create_all(engine)
