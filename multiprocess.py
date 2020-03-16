import multiprocessing as mp
import logging
from datetime import date, time, datetime, timedelta
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

import time

def job():
    logging.info("Processing : starting")
    for i in range(5):
        time.sleep(5)
    logging.info("Processing : stop",)
if(__name__=='__main__'):
    p = mp.Process(target=job)
    p.start()
    logging.info("Create Process")
    job()
    