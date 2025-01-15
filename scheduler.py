import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from main import main, purge, process_inbox_by_keywords

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()

    scheduler.add_job(main, trigger=IntervalTrigger(minutes=15))
    scheduler.add_job(process_inbox_by_keywords, trigger=IntervalTrigger(minutes=10))
    scheduler.add_job(purge, trigger=IntervalTrigger(hours=23))

    scheduler.start()
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass