
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from src.conf.config import settings


url_to_db = settings.postgres_url

engine = create_engine(url_to_db, echo=False, pool_size=5, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()
