from dateutil.relativedelta import relativedelta
import datetime
from RPA.Browser.Selenium import ElementNotFound, ElementClickInterceptedException


class NYTimesLocators:
    def __init__(self):
        self.SearchField = "searchTextField"
        self.SearchDropDownMenu = '//*[@data-testid="search-multiselect-button"]'
        self.CheckBoxSection = '//input[contains(@value,"{}")]'
        self.DateDropDownMenu = '//*[@data-testid="search-date-dropdown-a"]'
        self.NotificationBtn = '//*[@aria-label="Button to collapse the message"]'
        self.SpecificDate = '//*[@value="Specific Dates"]'
        self.StartDate = "startDate"
        self.EndDate = "endDate"
        self.RecentNewsOption = "//*[@class='css-v7it2b']"
        self.NewsAmount = '//*[@data-testid="SearchForm-status"]'
        self.NewsInfo = "//*[@data-testid='search-results']/li[{}]"
        self.ImageSrc = '//*[@id="site-content"]//li[{}]//img'
        self.BtnShowMore = '//*[@data-testid="search-show-more-button"]'


class NYTimesController:
    def __init__(self, driver, section, monthsago):
        self.driver = driver
        self.section = section
        self.monthsago = monthsago
        self.locators = NYTimesLocators()

    def closenotification(self):
        try:
            self.driver.click_element_when_visible(self.locators.NotificationBtn)

        except AssertionError:
            input("opa")
            pass

    def selectsections(self):
        """
        Method to select the Sections that the user wants
        """
        # Wait the element exists, then, click to open the CheckBox Menu
        self.driver.page_should_contain_element(self.locators.SearchField)
        self.driver.click_element(self.locators.SearchDropDownMenu)

        # Select the sections that the user wants

        for values in self.section:
            try:
                # This one uses Dynamically Locator, so, it's not in the self.locators Variable
                self.driver.click_element(self.locators.CheckBoxSection.format(values))

            except ElementNotFound:
                print(f"The Section : {values} does not exist, trying the next one")

    def filterdate(self):
        """
        Method to filter the News date that we want to see
        """
        # Open the date Menu
        self.driver.click_element(self.locators.DateDropDownMenu)

        # Click in specific Dates
        self.driver.click_element(self.locators.SpecificDate)

        # Wait for the input loads and then, insert the Start Date
        self.driver.page_should_contain_element(self.locators.StartDate)
        self.driver.press_keys(
            self.locators.StartDate,
            datetime.datetime.strftime(
                datetime.datetime.today() - relativedelta(months=self.monthsago),
                "%m/%d/%Y",
            ),
            "ENTER",
        )

        # Wait for the input loads and then, insert the End Date
        self.driver.page_should_contain_element(self.locators.EndDate)
        self.driver.press_keys(
            self.locators.EndDate,
            datetime.datetime.strftime(datetime.datetime.today(), "%m/%d/%Y"),
            "ENTER",
        )

    def selectrecentnews(self):
        """
        Method that select the Newest News
        """

        # Select the option Newest in the Dropdown Menu
        self.driver.select_from_list_by_value(self.locators.RecentNewsOption, "newest")

    def getnewsamount(self):
        """
        Method to get the Amount of News filtered
        """

        # Return the number of News
        return int(
            self.driver.get_text(self.locators.NewsAmount)
            .split()[1]
            .replace(",", "")
            .replace(".", "")
        )

    def getdata(self, index):
        """
        Method that get the Title of the news
        """
        # Wait for the Title element loads, then, return the title text
        self.driver.wait_until_element_is_visible(self.locators.NewsInfo.format(index))
        return self.driver.get_text(self.locators.NewsInfo.format(index))

    def getfilename(self, index):
        """
        Method that get the filename
        """
        return self.driver.get_element_attribute(
            self.locators.ImageSrc.format(index), "srcset"
        ).split(" ")[0]

    def clickshowmore(self):
        """
        Method that click in Show More
        """

        try:
            # Click in Show More
            self.driver.click_element_when_clickable(self.locators.BtnShowMore, timeout=2)

        except ElementNotFound or ElementClickInterceptedException:
            pass
