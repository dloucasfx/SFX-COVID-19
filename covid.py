import os.path
import csv
import urllib.request
import re
import datetime
import time
import json


class SFXCOVID19:

    def __init__(self, confirmed_url, deaths_url, recovered_url, last_sync_file="/opt/sfx_covid_19_lsd.json"):
        self.las_sync_file = last_sync_file
        self.last_sync = {}
        self.confirmed_url = confirmed_url
        self.deaths_url = deaths_url
        self.recovered_url = recovered_url

    def run(self):
        if os.path.exists(self.las_sync_file):
            with open(self.las_sync_file, 'r') as jsonFile:
                self.last_sync = json.load(jsonFile)
        else:
            self.last_sync = {
                "covid-19-confirmed": 0,
                "covid-19-deaths": 0,
                "covid-19-recovered": 0
            }

        self.sync_dps()

    def sync_dps(self):
        confirmed_dict = fetch_csv(self.confirmed_url)
        deaths_dict = fetch_csv(self.deaths_url)
        recovered_dict = fetch_csv(self.recovered_url)
        self.send_dps(confirmed_dict, "covid-19-confirmed", "ble")
        self.send_dps(deaths_dict, "covid-19-deaths", "ble")
        self.send_dps(recovered_dict, "covid-19-recovered", "ble")
        self.persist_last_sync()

        while True:
            time.sleep(3600)
            self.sync_dps()

    def send_dps(self, csvDict, metric, type):
        pattern = re.compile(r"\d{1,2}/\d{1,2}/\d{1,2}")
        last_sync_metric = self.last_sync[metric]
        for item in csvDict:
            dimensions = {}
            metrics = {}
            for k, v in item.items():
                if pattern.match(k):
                    metrics[k] = v
                else:
                    dimensions[k] = v
            for metric_date, metric_value in metrics.items():
                date_epoch = datetime.datetime.strptime(metric_date, "%m/%d/%y").timestamp() * 1000
                if date_epoch < last_sync_metric + 1:
                    continue
                else:
                    if self.last_sync[metric] < date_epoch:
                        self.last_sync[metric] = date_epoch
                    print(
                        "Metric {} --- sending dp : on {} with dimensions {} and value {}\n".format(metric, date_epoch,
                                                                                                    dimensions,
                                                                                                    metric_value))

    def persist_last_sync(self):
        last_sync = {
            "covid-19-confirmed": self.last_sync["covid-19-confirmed"],
            "covid-19-deaths": self.last_sync["covid-19-deaths"],
            "covid-19-recovered": self.last_sync["covid-19-recovered"]
        }
        with open(self.las_sync_file, 'w') as json_file:
            json.dump(last_sync, json_file)


def fetch_csv(url):
    file_name, headers = urllib.request.urlretrieve(url, "/tmp/{}".format(url.rsplit('/', 1)[-1]))
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        list_dict = []
        for line in csv_reader:
            list_dict.append(line)
    return list_dict


def main():
    confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
    deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
    recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
    sfx_corona = SFXCOVID19(confirmed_url, deaths_url, recovered_url, "/tmp/sfx_covid_19_lsd.json")
    sfx_corona.run()


if __name__ == "__main__":
    main()
