from crontab import CronTab
from datetime import datetime
cron = CronTab(user='plant')


def clear_all_jobs() -> int:  # Clear all Plant Jobs
    for job in cron:
        cron.remove(job)
    return 0


def create_jobs() -> int:  # Create All Plant Jobs
    jobs = []
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S ")

    # Make Poll Script
    jobs.append(
        cron.new(command='export PYTHONPATH=/home/plant/code/CareForMyPlant; /usr/bin/python3 ~/code/CareForMyPlant/src/jobs/poll.py >> /home/plant/logs/logs.txt 2>&1', comment=f"Cron Job Created At: {now}")
    )
    jobs[-1].setall('0 8 * * *')  # At 8am Every Day

    # Vote Counting Script
    jobs.append(
        cron.new(command='export PYTHONPATH=/home/plant/code/CareForMyPlant; /usr/bin/python3 /home/plant/code/CareForMyPlant/src/jobs/count.py >> /home/plant/logs/logs.txt 2>&1', comment=f"Cron Job Created At: {now}")
    )
    jobs[-1].setall('0 22 * * *')  # At 10pm Every Day

    # Morning Data Collection
    jobs.append(
        cron.new(
            command='export PYTHONPATH=/home/plant/code/CareForMyPlant; /usr/bin/python3 /home/plant/code/CareForMyPlant/src/jobs/collect_data.py >> /home/plant/logs/logs.txt 2>&1',
            comment=f"Cron Job Created At: {now}")
    )
    jobs[-1].setall('0 9 * * *')  # At 9am Every Day

    # Evening Data Collection
    jobs.append(
        cron.new(
            command='export PYTHONPATH=/home/plant/code/CareForMyPlant; /usr/bin/python3 /home/plant/code/CareForMyPlant/src/jobs/collect_data.py >> /home/plant/logs/logs.txt 2>&1',
            comment=f"Cron Job Created At: {now}")
    )
    jobs[-1].setall('0 16 * * *')  # At 4pm Every Day

    # Night Data Collection
    jobs.append(
        cron.new(
            command='export PYTHONPATH=/home/plant/code/CareForMyPlant; /usr/bin/python3 /home/plant/code/CareForMyPlant/src/jobs/collect_data.py >> /home/plant/logs/logs.txt 2>&1',
            comment=f"Cron Job Created At: {now}")
    )
    jobs[-1].setall('0 0 * * *')  # At 12am Every Day

    cron.write()
    return 0

