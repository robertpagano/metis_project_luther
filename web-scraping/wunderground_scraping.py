import os
os.mkdir('wund_html')

stations = ["KBIS","KFAR", "KGFK", "KDVL", "KJMS", "KMOT", "KISN"]
for station in stations:
    os.mkdir('wund_html/'+station)


from datetime import datetime, timedelta
from urllib.request import urlopen

def scrape_station(station, begin_date, end_date):
    current_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")+timedelta(days=1) #add one to make loop end on the end date
    
    
     # Use .format(station, YYYY, M, D)
    lookup_URL = 'http://www.wunderground.com/history/airport/{}/{}/{}/{}/DailyHistory.html'


    while current_date != end_date:

        if current_date.day == 1:
            print(str(current_date)+" "+str(station))

        formatted_lookup_URL = lookup_URL.format(station,
                                                 current_date.year,
                                                 current_date.month,
                                                 current_date.day)
        html = urlopen(formatted_lookup_URL).read().decode('utf-8')

        out_file_name = 'wund_html/{}/{}-{}-{}.html'.format(station, current_date.year,
                                                  current_date.month,
                                                  current_date.day)

        with open(out_file_name, 'w') as out_file:
            out_file.write(html)

        current_date += timedelta(days=1)

for station in stations:
        scrape_station(station, "2018-4-12", "2018-4-15")