import os
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker


DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

PG_DSN = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class SwapiPeaple(Base):
    __tablename__ = 'swapi_people'

    id = sa.Column(sa.Integer, primary_key=True)
    birth_year = sa.Column(sa.String)
    eye_color = sa.Column(sa.String)
    films = sa.Column(sa.String)
    gender = sa.Column(sa.String)
    hair_color = sa.Column(sa.String)
    height = sa.Column(sa.String)
    homeworld = sa.Column(sa.String)
    mass = sa.Column(sa.String)
    name = sa.Column(sa.String)
    skin_color = sa.Column(sa.String)
    species = sa.Column(sa.String)
    starships = sa.Column(sa.String)
    vehicles = sa.Column(sa.String)

