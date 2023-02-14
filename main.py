from fastapi import FastAPI
from facebook import GraphAPI
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


Base = declarative_base()

class FacebookPage(Base):
    __tablename__ = 'facebook_pages'

    id = Column(Integer, primary_key=True)
    page_id = Column(String, unique=True)
    data = Column(JSON)

engine = create_engine('sqlite:///facebook.db')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

app = FastAPI()

page_id = os.getenv("PAGE_ID")
access_token = os.getenv("ACCESS_TOKEN")

@app.get("/{page_id}")
async def scrape_facebook_page(page_id: str):
    
    graph = GraphAPI(access_token)

    fields = "id, name, about, description, fan_count,location,likes,posts, picture"
    page_data = graph.get_object(page_id, fields=fields)

    page = session.query(FacebookPage).filter_by(page_id=page_id).first()
    if page is None:
        page = FacebookPage(page_id=page_id, data=page_data)
        session.add(page)
    else:
        page.data = page_data
    session.commit()

    return {"data": page_data}
