from time import sleep
from dateutil.relativedelta import relativedelta
import datetime


class NYTimesController:

    def __init__(self,driver,section,MonthsAgo):
        self.driver = driver
        self.section = section
        self.MonthsAgo = MonthsAgo
        self.Locators = {
                            "Sections":{
                                "SearchField":"searchTextField",
                                "DropDownMenu":'data-testid="search-multiselect-button"',
                            },

                            "Date":{
                                "DropDownMenu":'data-testid="search-date-dropdown-a"',
                                "SpecificDate":'value="Specific Dates"',
                                "StartDate":"startDate",
                                "EndDate":"endDate"
                            },
                            
                            "RecentNews":{
                                "Option":"//*[@class='css-v7it2b']"
                            },

                            "NewsAmount":{
                                "News":'data-testid="SearchForm-status"'
                            },

                            "NewsData":{
                                "NewsInfo":"//*[@data-testid='search-results']/li"
                            },

                            "Filename":{
                                "Src":'data-testid="search-bodega-result"'
                            },

                            "ShowMore":{
                                "BtnShowMore":'data-testid="search-show-more-button"'
                            }
                        }


    def SelectSections(self):
        """
        Method to select the Sections that the user wants
        """
        try:

            # Wait the element exists, then, click to open the CheckBox Menu
            self.driver.page_should_contain_element(self.Locators["Sections"]["SearchField"])
            self.driver.execute_javascript(f'document.querySelector(`[{self.Locators["Sections"]["DropDownMenu"]}]`).click()')
            
            #Select the sections that the user wants

            for values in self.section:
                try:
                    #This one uses Dynamically Locator, so, it's not in the Locators Variable
                    self.driver.click_element(f'//input[contains(@value,"{values}")]')

                except:
                    print(f"The Section : {values} does not exist, trying the next one")


        except Exception as error:
            raise Exception(f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}")


    def FilterDate(self):
        """
            Method to filter the the News date that we want to see
        """

        try:
            
            #Open the date Menu
            self.driver.execute_javascript(f'document.querySelector(`[{self.Locators["Date"]["DropDownMenu"]}]`).click()')
            sleep(2)

            #Click in specific Dates
            self.driver.execute_javascript(f'document.querySelector(`[{self.Locators["Date"]["SpecificDate"]}]`).click()')


            #Wait for the input loads and then, insert the Start Date
            self.driver.page_should_contain_element(self.Locators["Date"]["StartDate"])
            self.driver.press_keys("startDate",datetime.datetime.strftime(datetime.datetime.today() - relativedelta(months=self.MonthsAgo),"%m/%d/%Y"),'ENTER')


            #Wait for the input loads and then, insert the End Date
            self.driver.page_should_contain_element(self.Locators["Date"]["EndDate"])
            self.driver.press_keys("endDate",datetime.datetime.strftime(datetime.datetime.today(),"%m/%d/%Y"),'ENTER')

            sleep(5)


        except Exception as error:
            raise Exception(f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}")


    def SelectRecentNews(self):
            """
                Method that select the Newest News
            """
            
            #Select the option Newest in the Dropdown Menu
            try:
                self.driver.select_from_list_by_value(self.Locators["RecentNews"]["Option"],"newest")
            

            except Exception as error:
                raise Exception(f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}")

    
    def GetNewsAmount(self):
        """
            Method to get the Amount of News filtered
        """

        #Return the number of News
        try:
            return int(self.driver.execute_javascript(f'return document.querySelector(`[{self.Locators["NewsAmount"]["News"]}]`).innerText').split()[1].replace(',',''))


        except Exception as error:
            raise Exception(f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}")


    def GetData(self,index):
        """
            Method that get the Title of the news
        """
        try:
            self.driver.page_should_contain_element(self.Locators["NewsData"]["NewsInfo"]+f"[{index}]")
            

            #Wait for the Title element loads, then, return the title text
            return self.driver.get_text(self.Locators["NewsData"]["NewsInfo"]+f"[{index}]")
        

        except Exception as error:
            raise Exception(f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}")

        
    def GetFilename(self,Title):
        """
            Method that get the filename
        """

        try:
            #Return the file src
            return self.driver.execute_javascript(f'return [...document.querySelectorAll(`[{self.Locators["Filename"]["Src"]}]`)].find(e => e.innerText.includes("{Title}")).childNodes[0].childNodes[1].childNodes[1].childNodes[0].childNodes[0].srcset').split(' ')[0]


        except Exception as error:
            raise Exception(f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}")
        

    def ClickShowMore(self):
        """
            Method that click in Show More
        """

        try:
            #Click in Show More
            self.driver.execute_javascript(f'document.querySelector(`[{self.Locators["ShowMore"]["BtnShowMore"]}]`).click()')

        except Exception as error:
            raise Exception(f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}")
