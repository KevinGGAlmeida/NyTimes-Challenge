from time import sleep
from dateutil.relativedelta import relativedelta
import datetime


class NyTimesLocators:
    SearchField = "searchTextField"
    SearchDropDownMenu = '//*[@data-testid="search-multiselect-button"]'
    CheckBoxSection = '//input[contains(@value,"{}")]'
    DateDropDownMenu = '//*[@data-testid="search-date-dropdown-a"]'
    NotificationBtn = '//*[@aria-label="Button to collapse the message"]'
    SpecificDate = '//*[@value="Specific Dates"]'
    StartDate = "startDate"
    EndDate = "endDate"
    RecentNewsOption = "//*[@class='css-v7it2b']"
    NewsAmount = '//*[@data-testid="SearchForm-status"]'
    NewsInfo = "//*[@data-testid='search-results']/li[{}]"
    ImageSrc = '//*[@id="site-content"]//li[{}]//img'
    BtnShowMore = '//*[@data-testid="search-show-more-button"]'


class NYTimesController:
    def __init__(self, driver, section, MonthsAgo):
        self.driver = driver
        self.section = section
        self.MonthsAgo = MonthsAgo

    def CloseNotification(self):
        try:
            self.driver.page_should_contain_element(NyTimesLocators.NotificationBtn)
            self.driver.click_element(NyTimesLocators.NotificationBtn)

        except Exception as error:
            pass

    def SelectSections(self):
        """
        Method to select the Sections that the user wants
        """
        try:
            # Wait the element exists, then, click to open the CheckBox Menu
            self.driver.page_should_contain_element(NyTimesLocators.SearchField)
            self.driver.click_element(NyTimesLocators.SearchDropDownMenu)

            # Select the sections that the user wants

            for values in self.section:
                try:
                    # This one uses Dynamically Locator, so, it's not in the Locators Variable
                    self.driver.click_element(
                        NyTimesLocators.CheckBoxSection.format(values)
                    )

                except:
                    print(f"The Section : {values} does not exist, trying the next one")

        except Exception as error:
            raise Exception(
                f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}"
            )

    def FilterDate(self):
        """
        Method to filter the the News date that we want to see
        """

        try:
            # Open the date Menu
            self.driver.click_element(NyTimesLocators.DateDropDownMenu)
            sleep(2)

            # Click in specific Dates
            self.driver.click_element(NyTimesLocators.SpecificDate)

            # Wait for the input loads and then, insert the Start Date
            self.driver.page_should_contain_element(NyTimesLocators.StartDate)
            self.driver.press_keys(
                NyTimesLocators.StartDate,
                datetime.datetime.strftime(
                    datetime.datetime.today() - relativedelta(months=self.MonthsAgo),
                    "%m/%d/%Y",
                ),
                "ENTER",
            )

            # Wait for the input loads and then, insert the End Date
            self.driver.page_should_contain_element(NyTimesLocators.EndDate)
            self.driver.press_keys(
                NyTimesLocators.EndDate,
                datetime.datetime.strftime(datetime.datetime.today(), "%m/%d/%Y"),
                "ENTER",
            )

            sleep(5)

        except Exception as error:
            raise Exception(
                f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}"
            )

    def SelectRecentNews(self):
        """
        Method that select the Newest News
        """

        # Select the option Newest in the Dropdown Menu
        try:
            self.driver.select_from_list_by_value(
                NyTimesLocators.RecentNewsOption, "newest"
            )

        except Exception as error:
            raise Exception(
                f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}"
            )

    def GetNewsAmount(self):
        """
        Method to get the Amount of News filtered
        """

        # Return the number of News
        try:
            return int(
                self.driver.get_text(NyTimesLocators.NewsAmount)
                .split()[1]
                .replace(",", "")
                .replace(".", "")
            )

        except Exception as error:
            raise Exception(
                f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}"
            )

    def GetData(self, index):
        """
        Method that get the Title of the news
        """
        try:
            self.driver.page_should_contain_element(
                NyTimesLocators.NewsInfo.format(index)
            )

            # Wait for the Title element loads, then, return the title text
            return self.driver.get_text(NyTimesLocators.NewsInfo.format(index))

        except Exception as error:
            raise Exception(
                f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}"
            )

    def GetFilename(self, index):
        """
        Method that get the filename
        """

        try:
            return self.driver.get_element_attribute(
                NyTimesLocators.ImageSrc.format(index), "srcset"
            ).split(" ")[0]

        except Exception as error:
            raise Exception(
                f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}"
            )

    def ClickShowMore(self):
        """
        Method that click in Show More
        """

        try:
            # Click in Show More
            self.driver.click_element(NyTimesLocators.BtnShowMore)

        except Exception as error:
            raise Exception(
                f"Error: {str(error)}\n Line error: {error.__traceback__.tb_lineno}"
            )
