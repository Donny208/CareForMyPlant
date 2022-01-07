import os
from src.classes.reddit import Reddit
from src.jobs.water_plant import *
from dotenv import load_dotenv
load_dotenv()

reddit = Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME")
)

results = reddit.tally_votes()

# If the users vote yes, water the plant
if results:
    water_plant(15)
