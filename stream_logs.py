from faker import Faker
import time
import random
import os
import numpy as np
from datetime import datetime, timedelta



LINE = """\
{remote_addr} - - [{time_local}] "{request_type} {request_path} HTTP/1.1" [{status}] {body_bytes_sent} "{http_referer}" "{http_user_agent}"\
"""


log_fileD = "user_log_fileD.txt";

def generate_log_line():
    fake = Faker()
    now = datetime.now()
    remote_addr = fake.ipv4()
    time_local = now.strftime('%d/%b/%Y:%H:%M:%S')
    request_type = random.choice(["GET", "POST", "PUT"])
    request_path = "/" + fake.uri_path()

    status = random.choice([200, 401, 404])
    body_bytes_sent = random.choice(range(5, 1000, 1))
    http_referer = fake.uri()
    http_user_agent = fake.user_agent()

    log_line = LINE.format(
        remote_addr=remote_addr,
        time_local=time_local,
        request_type=request_type,
        request_path=request_path,
        status=status,
        body_bytes_sent=body_bytes_sent,
        http_referer=http_referer,
        http_user_agent=http_user_agent
    )

    return log_line

def write_log_line(log_file, line):
    with open(log_file, "a") as f:
        f.write(line)
        f.write("\n")

def clear_log_file(log_file):
    with open(log_file, "w+") as f:
        f.write("")

if __name__ == "__main__":
    current_log_file = log_fileD
    lines_written = 0

    # clear_log_file(LOG_FILE_A)
    # clear_log_file(LOG_FILE_B)

    while True:
        line = generate_log_line()
        print(line)

        #write_log_line(current_log_file, line)
        lines_written += 1

        sleep_time = random.choice(range(1, 3, 1))

        time.sleep(sleep_time)
