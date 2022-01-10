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



def dump_json_to_pdf():
    clear_terminal()
    f = BytesIO()
    pdf = PDFDocument(f)
    pdf.init_report()

    try:
        with open('all-time-lows.json') as json_file:
            data = json.load(json_file)
        print("Successfully loaded!")
    except:
        print("Failed to load JSON!")

    for title in data:
        
        pdf.h1(title)
        for product in data[title]:
            pdf.p("Store: " + str(product["store"]))
            pdf.p("Price: " + str(product["price"]))
            pdf.p("URL: " + str(product["url"]))
            pdf.p("\n")
        
        pdf.p("\n\n")

    pdf.generate()
    input("\nPress [ENTER] to continue: ")