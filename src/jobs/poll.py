import os
from src.classes.reddit import Reddit
from dotenv import load_dotenv
load_dotenv()

reddit = Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME")
)

reddit.create_poll(25)
