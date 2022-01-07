import os
from crontab import CronTab
from datetime import datetime

cron = CronTab(user='plant')
env = "prod" if '/prod/' in os.path.dirname(__file__) else "dev"


def clear_all_jobs() -> int:  # Clear all Plant Jobs
    for job in cron:
        cron.remove(job)
    return 0


def create_jobs() -> int:  # Create All Plant Jobs
    jobs = []
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S ")

    # Make Poll Script
    jobs.append(
        cron.new(command=f'export PYTHONPATH=/home/plant/{env}/CareForMyPlant; /usr/bin/python3 '
                         f'~/{env}/CareForMyPlant/src/jobs/poll.py >> /home/plant/logs/logs.txt 2>&1', 
                 comment=f"Cron Job Created At: {now}")
    )
    jobs[-1].setall('0 8 * * *')  # At 8am Every Day

    # Vote Counting Script
    jobs.append(
        cron.new(command=f'export PYTHONPATH=/home/plant/{env}/CareForMyPlant; /usr/bin/python3 '
                         f'/home/plant/{env}/CareForMyPlant/src/jobs/count.py >> /home/plant/logs/logs.txt 2>&1',
                 comment=f"Cron Job Created At: {now}")
    )
    jobs[-1].setall('0 22 * * *')  # At 10pm Every Day

    # Morning Data Collection
    jobs.append(
        cron.new(
            command=f'export PYTHONPATH=/home/plant/{env}/CareForMyPlant; /usr/bin/python3 '
                    f'/home/plant/{env}/CareForMyPlant/src/jobs/collect_data.py >> /home/plant/logs/logs.txt 2>&1',
            comment=f"Cron Job Created At: {now}")
    )
    jobs[-1].setall('0 9 * * *')  # At 9am Every Day

    # Evening Data Collection
    jobs.append(
        cron.new(
            command=f'export PYTHONPATH=/home/plant/{env}/CareForMyPlant; /usr/bin/python3 '
                    f'/home/plant/{env}/CareForMyPlant/src/jobs/collect_data.py >> /home/plant/logs/logs.txt 2>&1',
            comment=f"Cron Job Created At: {now}")
    )
    jobs[-1].setall('0 16 * * *')  # At 4pm Every Day

    # Night Data Collection
    jobs.append(
        cron.new(
            command=f'export PYTHONPATH=/home/plant/{env}/CareForMyPlant; /usr/bin/python3 '
                    f'/home/plant/{env}/CareForMyPlant/src/jobs/collect_data.py >> /home/plant/logs/logs.txt 2>&1',
            comment=f"Cron Job Created At: {now}")
    )
    jobs[-1].setall('0 0 * * *')  # At 12am Every Day

    cron.write()
    return 0

