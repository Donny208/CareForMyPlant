# Libraries
import os
from dotenv import load_dotenv

# Scripts
from src.scripts.cronSetup import clear_all_jobs, create_jobs

# Classes
from src.classes.reddit import Reddit
from src.classes.miflora import MiFlora

# Pre-Setup
load_dotenv()

reddit = Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME")
)

# Cron Job Setup
print("-> Cron Jobs")
if clear_all_jobs() == 0:
    print("\t->Jobs Cleared")
if create_jobs() == 0:
    print("\t->Jobs Successfully Created")



### TESTING SECTION ####
# print("\n\n\nTESTING!!!\n\n\n")
#reddit.create_poll(25)
# #reddit.tally_votes()
#print(reddit.get_water_history(15))