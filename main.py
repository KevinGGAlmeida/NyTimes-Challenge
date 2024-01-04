from RPA.Browser.Selenium import Selenium, ElementNotFound
from functions import NYTimesController
import pandas as pd
import urllib.request
import urllib.error
from pathlib import Path
import yaml
from robocorp.tasks import task


class Nytimes:
    def __init__(
        self, site, searchphrase, sections, monthsago, controller, numberofnews
    ):
        self.site = site
        self.monthsago = monthsago
        self.searchphrase = searchphrase
        self.sections = sections
        self.driver = Selenium()
        self.numberofnews = numberofnews
        self.controller = controller(self.driver, self.sections, self.monthsago)
        self.df = pd.DataFrame(
            columns=[
                "News Title",
                "News Description",
                "News Date",
                "News Filename",
                "Word Ocurrences",
                "News Includes Cash?",
            ]
        )

    def launch(self):
        self.driver.open_available_browser(f"{self.site}{self.searchphrase}")

    def navigation(self):
        self.controller.closenotification()
        self.controller.selectsections()
        self.controller.selectrecentnews()
        self.controller.filterdate()
        
        for index in range(1, self.numberofnews + 1):
            print(index)
            try:
                # Click in SHOW MORE
                self.controller.clickshowmore()

                # Get Date, Title and Description
                info = self.controller.getdata(index).split("\n")

                # Try download the image
                try:
                    filename = self.controller.getfilename(index)
                    urllib.request.urlretrieve(
                        filename, f"{Path.cwd()}/output/{info[2]}.{filename[-4:]}"
                    )

                except urllib.error.URLError:
                    filename = "No image"

                # Validating how many times the Phrase searched appears in the Description or Title
                repeated_words_qtd = info[2].count(self.searchphrase) + info[3].count(
                    self.searchphrase
                )

                # Validating if the description or title has CASH included

                cash = (
                    "true"
                    if any(
                        valor in info[2] + info[3] for valor in ["$", "dollar", "usd"]
                    )
                    else "false"
                )

                # Appending the information to the DataFrame
                self.df.loc[len(self.df)] = [
                    info[2],
                    info[3],
                    info[0],
                    f"{info[2]}{filename[-4:]}" if filename != "No image" else filename,
                    repeated_words_qtd,
                    cash,
                ]

            except ElementNotFound:
                print("Line of Advertisement")

        self.df.to_excel(f"{Path.cwd()}/output/News.xlsx", index=False)

    def closewindow(self):
        self.driver.close_browser()


@task
def task():
    with open('config.yaml', 'r') as file:
        configfile = yaml.safe_load(file)


    run = Nytimes(
        configfile["Parameters"]["Url"],
        configfile["Parameters"]["SearchPhrase"],
        configfile["Parameters"]["Sections"],
        configfile["Parameters"]["MonthsAgoSearch"],
        NYTimesController,
        configfile["Parameters"]["NewsAmount"],
    )
    run.launch()
    run.navigation()
    run.closewindow()
