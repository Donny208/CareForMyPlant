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
                 comment=f"Cron Job Created At: {now} | Poll Script")
    )
    jobs[-1].setall('0 8 * * *')  # At 8am Every Day

    # Vote Counting Script
    jobs.append(
        cron.new(command=f'export PYTHONPATH=/home/plant/{env}/CareForMyPlant; /usr/bin/python3 '
                         f'/home/plant/{env}/CareForMyPlant/src/jobs/count.py >> /home/plant/logs/logs.txt 2>&1',
                 comment=f"Cron Job Created At: {now} | Vote Tally Script")
    )
    jobs[-1].setall('0 22 * * *')  # At 10pm Every Day

    # Morning Data Collection
    jobs.append(
        cron.new(
            command=f'export PYTHONPATH=/home/plant/{env}/CareForMyPlant; /usr/bin/python3 '
                    f'/home/plant/{env}/CareForMyPlant/src/jobs/collect_data.py >> /home/plant/logs/logs.txt 2>&1',
            comment=f"Cron Job Created At: {now} | Morning Data Collection")
    )
    jobs[-1].setall('0 9 * * *')  # At 9am Every Day

    # Evening Data Collection
    jobs.append(
        cron.new(
            command=f'export PYTHONPATH=/home/plant/{env}/CareForMyPlant; /usr/bin/python3 '
                    f'/home/plant/{env}/CareForMyPlant/src/jobs/collect_data.py >> /home/plant/logs/logs.txt 2>&1',
            comment=f"Cron Job Created At: {now} | Evening Data Collection")
    )
    jobs[-1].setall('0 16 * * *')  # At 4pm Every Day

    # Night Data Collection
    jobs.append(
        cron.new(
            command=f'export PYTHONPATH=/home/plant/{env}/CareForMyPlant; /usr/bin/python3 '
                    f'/home/plant/{env}/CareForMyPlant/src/jobs/collect_data.py >> /home/plant/logs/logs.txt 2>&1',
            comment=f"Cron Job Created At: {now} | Night Data Collection")
    )
    jobs[-1].setall('0 0 * * *')  # At 12am Every Day

    # Backups
    jobs.append(
        cron.new(
            command=f'mongoexport --collection=data --db=plant --out=/home/plant/usb/data.json;'
                    f'mongoexport --collection=users --db=plant --out=/home/plant/usb/users.json;'
                    f'mongoexport --collection=votes --db=plant --out=/home/plant/usb/votes.json',
            comment=f"Cron Job Created At: {now} | Data Backup")
    )
    jobs[-1].setall('30 1 * * *')  # At 1:30am Every Day

    # Reboot
    jobs.append(
        cron.new(
            command='sudo reboot',
            comment=f"Cron Job Created At: {now} | Pi Reboot")
    )
    jobs[-1].setall('0 20 * * 1')  # At 8pm On Monday

    if env == 'prod':
        # Git Pulling new updates
        jobs.append(
            cron.new(
                command=f'git -C ~/{env}/CareForMyPlant/ pull',
                comment=f"Cron Job Created At: {now} | Git Pull")
        )
        jobs[-1].setall('0 1 * * *')  # At 1am Every Day

    cron.write()
    return 0

