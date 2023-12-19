from RPA.Browser.Selenium import Selenium
from functions import NYTimesController
from time import sleep
import pandas as pd
import urllib.request


class Nytimes:
    
    def __init__(self,site,SearchPhrase,Sections,MonthsAgo,Controller):
        self.site = site
        self.MonthsAgo = MonthsAgo
        self.SearchPhrase = SearchPhrase
        self.sections = Sections
        self.driver = Selenium()
        self.Controller = Controller(self.driver,self.sections,self.MonthsAgo)


    def launch(self):
        self.driver.open_available_browser(f"{self.site}{self.SearchPhrase}")
        self.driver.maximize_browser_window()


    def Data(self):
        self.df = pd.DataFrame(columns=["News Title","News Description","News Date","News Filename","Word Ocurrences","News Includes Cash?"])

    
    def Navigation(self):
        self.Controller.SelectSections()
        self.Controller.SelectRecentNews()
        self.Controller.FilterDate()
        sleep(5)
        
        for index in range(1,self.Controller.GetNewsAmount() + 1):

            try:

                #Click in SHOW MORE
                try:
                    self.Controller.ClickShowMore()
                except:
                    pass

                
                #Get Date, Title and Description
                self.Info = self.Controller.GetData(index).split("\n")


                #Try download the image
                try:
                    self.filename = self.Controller.GetFilename(self.Info[2])
                    urllib.request.urlretrieve(self.filename, f"{self.Info[2]}.{self.filename[-4:]}")
                

                except:
                    self.filename = "No image"


                #Validating how many times the Phrase searched appears in the Description or Title
                self.Times = self.Info[2].count(self.SearchPhrase) + self.Info[3].count(self.SearchPhrase)
                

                #Validating if the description or title has CASH included
                self.Cash = [True if "$" in valor or "dollar" in valor.lower() or "usd" in valor.lower() or "dollars" in valor.lower() else False for valor in [self.Info[3],self.Info[2]] ]
                

                #Appending the informations to the DataFrame
                self.df.loc[len(self.df)] =[self.Info[2],self.Info[3],self.Info[0],f"{self.Info[2]}{self.filename[-4:]}" if self.filename != "No image" else self.filename,self.Times,'true' if True in self.Cash else 'false']


            except Exception as error:
                print(str(error),error.__traceback__.tb_lineno,f"New's Line: {index}")
                print("Line of ADVERTISEMENT")


        self.df.to_excel("News.xlsx")


    def CloseWindow(self):
        self.driver.close_browser()


for Tries in range(3):
    try:
        Run = Nytimes("https://www.nytimes.com/search?query=","car",["Technology","Business"],4,NYTimesController)
        Run.Data()
        Run.launch()
        Run.Navigation()
        Run.CloseWindow()
        break

    except:
        Run.CloseWindow()

        if Tries == 2:
            raise

        else:
            print("An error Occurred, Trying again")
            