import os

from crontab import CronTab

cron = CronTab()
command = f'python {os.getcwd()}\main.py'
print(command)
job = cron.new(command=command)
job.day.every(1)

cron.write()
