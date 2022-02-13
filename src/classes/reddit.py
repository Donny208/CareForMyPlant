import praw
import datetime
import calendar
import random
from src.other.strings import string_data
from src.database.schema import *


class Reddit:
    def __init__(self, client_id, client_secret, password, user_agent, username):
        self.api = praw.Reddit(client_id=client_id, client_secret=client_secret,
                               password=password, user_agent=user_agent,
                               username=username)
        self.api.validate_on_submit = True

    def get_suffix(self, myDate) -> str:
        date_suffix = ["th", "st", "nd", "rd"]
        if myDate % 10 in [1, 2, 3] and myDate not in [11, 12, 13]:
            return date_suffix[myDate % 10]
        else:
            return date_suffix[0]

    def get_full_time(self) -> str:
        now = ((datetime.datetime.now()) - (datetime.timedelta(hours=7)))
        dayOfWeek = calendar.day_name[now.weekday()]
        month = calendar.month_name[now.month]
        day = now.day
        full_time = dayOfWeek + ", " + month + " " + str(day) + self.get_suffix(day)
        return full_time

    def get_date(self) -> str:
        return datetime.date.today().strftime("%Y/%m/%d")

    def get_water_history(self, n: int) -> str:
        votes = Vote.objects().order_by('-date').limit(n)
        fmt_str = string_data['water_history']
        for v in reversed(votes):
            fmt_str += f"{v.date} | {'✔️' if v.outcome == 1 else '❌'}\n"
        return fmt_str

    def get_plant_age(self) -> int:
        return abs((datetime.datetime.today() - datetime.datetime(2020, 5, 13, 10)).days)

    def get_voter_history(self, n: int) -> str:
        top_voters = sorted(User.objects(), key=lambda user: user.votes[0]+user.votes[1], reverse=True)[:n]
        str_fmt = string_data['top_voter_header']
        for voter in top_voters:
            str_fmt += f"{voter.username} | {str(voter.streak)} |{voter.votes[0]+voter.votes[1]} | {voter.votes[1]} " \
                       f"| {voter.votes[0]} | {ratio_check(voter.votes[1], voter.votes[0])}\n"
        return str_fmt

    def vote_validate(self, comment: praw.reddit.Comment, vote: Vote) -> None:
        if comment.author.name in vote.details.keys():
            print(f"\t-> {comment.author.name} already has voted")
            return
        users_vote = None

        # Checking if the vote is negative
        if comment.body.lower().strip() in string_data['accepted_votes'][0]:
            users_vote = 0
        # Checking if the vote is positive
        elif comment.body.lower().strip() in string_data['accepted_votes'][1]:
            users_vote = 1
        else:
            print(f"\t-> {comment.author}'s vote rejected: {users_vote}")
            return

        # Getting voter info
        user_query = User.objects(username=comment.author.name)

        # Updating User Data
        # User doesn't exist
        if len(user_query) == 0:
            user = User()
            user.username = comment.author.name
        else:
            user = user_query.first()

        user.votes[users_vote] += 1
        user.streak += 1
        user.save()

        vote.voters.append(user)
        vote.details[user.username] = users_vote
        vote.save()

        print(f"\t-> {user.username}'s vote of {str(users_vote)} was saved.")

    def create_poll(self, n_voters) -> None:
        plant_data = Data.objects().order_by('-timestamp').limit(1).first()
        postStr = "# Should I Be Watered Today?\n" \
                  "## **How To Vote**\n\n" \
                  f"{string_data['how_to_vote']}\n\n---\n" \
                  "## **Watering History**\n\n" \
                  f"{self.get_water_history(25)}\n\n---\n" \
                  f"## **Top {n_voters} Voters**\n\n" \
                  f"{self.get_voter_history(15)}\n\n---\n" \
                  "## **Other Info**\n\n" \
                  f"Plant's Age: {str(self.get_plant_age())} Days\n\n" \
                  f"Temperature: {str(plant_data.temperature)}°C ({str(round(plant_data.temperature * 1.8 + 32, 2))}°F)\n\n" \
                  f"Soil Moisture(Top Soil): {str(plant_data.moisture)}%\n\n" \
                  f"{string_data['development']}\n\n---\n{string_data['follow']}"

        # Making the post
        post = self.api.subreddit("careformyplant").submit(
            f"Should I be Watered Today: {self.get_full_time()}?", selftext=postStr)
        print(f"Poll Post Created: {post.id}")

        # Saving the vote to the database
        vote = Vote()
        vote.date = self.get_date()
        vote.post_id = post.id
        vote.save()

    def tally_votes(self) -> int:
        print("-> Tallying Votes")
        vote_query = Vote.objects(outcome=-1).first()
        if len(vote_query) > 1:
            print(f"\t-> Multiple Database instances of a Non-Tallied Vote, check DB.")
            return 1

        # Fetching Info
        vote = vote_query.first()
        reddit_post = self.api.submission(id=vote.post_id)

        root_comments = [x for x in reddit_post.comments if x.is_root and x.author.name != "literally_plant"]

        # Saving the volid votes
        for comment in root_comments:
            self.vote_validate(comment, vote)

        # Reloading Votes
        vote.reload()

        # Tallying the votes
        result_tally = [0, 0]
        for user in vote.details.keys():
            result_tally[vote.details[user]] += 1

        # Seeing which vote wins
        if result_tally[0] > result_tally[1]:  # Negative vote wins
            result = 0
        elif result_tally[0] < result_tally[1]:  # Positive vote wins
            result = 1
        else:  # Tie, random choice
            result = random.randrange(0, 2)

        # Saving our results
        vote.outcome = result
        vote.save()

        # Commenting the results in the thread
        reddit_post.reply(f"**Results:**\n\nYes|No\n:--|:--\n"
                          f"{str(result_tally[1])}|{str(result_tally[0])}\n\n"
                          f"*^(Poll Closed, check for a new post at 8:00"
                          f" Mountain time)*").mod.distinguish(how='yes', sticky=True)

        # Removing Streaks from people who didn't vote
        User.objects(username__not__in=vote.details.keys()).update(set__streak=0)

        print("\t-> Tally Complete")
        return result


def ratio_check(pos: int, neg: int) -> float:
    return round(pos / neg, 3) if neg else 0
