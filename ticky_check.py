#!/usr/bin/env python3

import re
import csv
import operator

error = {}
per_user = {}
logfile =r"/home/zubairfaris/Documents/python-interact-os/syslog.log"
pattern=r": ([A-Z]*) ([\w ']*) [\[\#\d\] ]*\(([\w\.]*)\)$"

with open(logfile, "r") as file:
  for line in file.readlines():
    result = re.search(pattern, line)
    log_type = result.group(1)
    log_message = result.group(2)
    log_user = result.group(3)

    if log_type == 'ERROR':
      if log_message in error:
        error[log_message] += 1
      else:
        error[log_message] = 1

    if log_user in per_user:
      if log_type == 'ERROR':
        per_user[log_user][log_type] += 1
      elif log_type == 'INFO':
        per_user[log_user][log_type] += 1
    else:
      if log_type == 'ERROR':
        per_user[log_user] = {"ERROR": 1, "INFO": 0}
      elif log_type == 'INFO':
        per_user[log_user] = {"ERROR": 0, "INFO": 1}

per_user = sorted(per_user.items())
error = sorted(error.items(), key = operator.itemgetter(1), reverse = True)

print(per_user)
print(error)

with open("error_message.csv", "w+") as error_csv:
  writer = csv.writer(error_csv)
  writer.writerow(["Error","Count"])
  writer.writerows(error)

with open("user_statistics.csv", "w+") as users_csv:
  writer = csv.writer(users_csv)
  writer.writerow(["Username", "INFO", "ERROR"])
  for item in per_user:
    user, log_type = item
    line = [user, log_type["INFO"], log_type["ERROR"]]
    writer.writerow(line)
