import datetime
import time

times = ['01:00:00']
now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")



if current_time in times:
    print("scrape")
else:
    current_raw_time = datetime.datetime.strptime(current_time, "%H:%M:%S")
    cur_lowest_diff = float('inf')

    for timeVal in times:
        sched_time = datetime.datetime.strptime(timeVal, "%H:%M:%S")
        diff = sched_time - current_raw_time
        secs_duration = diff.total_seconds()

        if secs_duration < cur_lowest_diff:
            cur_lowest_diff = secs_duration
            if cur_lowest_diff < 0:
                cur_lowest_diff = 86400 - (cur_lowest_diff * -1)

    print("Timestamp: " + str(now))
    print("Sleeping for: " + str ((cur_lowest_diff)/60) + " minutes")
    time.sleep(cur_lowest_diff)