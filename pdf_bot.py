from time import sleep
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import PyPDF2
import requests

FILE_SAVER_MIN_JS_URL = "https://raw.githubusercontent.com/eligrey/FileSaver.js/master/dist/FileSaver.min.js"

file_saver_min_js = requests.get(FILE_SAVER_MIN_JS_URL).content


class PDFBot():
    def __init__(self):
        # change the path file to the directory where you would like to place the downloaded file
        self.download_dir = "~/Documents/Springer_Books"

        # Initiating the Chrome driver
        self.urls = []

        # Initializing the PDF file and the respective variables
        self.pdf_file = open("/home/frank/Documents/Springer Ebooks.pdf", 'rb')
        self.pdf = PyPDF2.PdfFileReader(self.pdf_file)
        self.pages = self.pdf.getNumPages()
        self.key = '/Annots'
        self.uri = '/URI'
        self.ank = '/A'

    def get_hyperlinks_from_pdf(self):

        for page in range(self.pages):
            # print("Current Page: {}".format(page)) # Useful when listing it for visualization
            self.pageSliced = self.pdf.getPage(page)
            self.pageObject = self.pageSliced.getObject()
            if self.key in self.pageObject.keys():
                self.annotation = self.pageObject[self.key]
                try:
                    for self.item in self.annotation:
                        self.url = self.item.getObject()
                        if self.uri in self.url[self.ank].keys():
                            # print(self.u[self.ank][self.uri]) # Printing content
                            self.urls.append(self.url[self.ank][self.uri])
                except KeyError:
                    pass

        # print(self.urls) # Including all urls in a list

    def download_wait(self, directory, timeout, nfiles=None):
        """
        Wait for downloads to finish with a specified timeout.

        Args
        ----
        directory : str
            The path to the folder where the files will be downloaded.
        timeout : int
            How many seconds to wait until timing out.
        nfiles : int, defaults to None
            If provided, also wait for the expected number of files.

        """
        seconds = 0
        dl_wait = True
        while dl_wait:  # or seconds < timeout:
            sleep(1)
            dl_wait = False
            files = os.listdir(directory)
            if nfiles and len(files) != nfiles:
                dl_wait = True

            for fname in files:
                if fname.endswith('.crdownload'):
                    dl_wait = True

            seconds += 0
        return seconds

    def download_books(self):
        # Function to handle setting up headless download
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_experimental_option('prefs',
                                               {"download.default_directory": "/home/frank/Documents/Springer_Books",
                                                "download.prompt_for_download": False,
                                                "download.directory_upgrade": True,
                                                "plugins.always_open_pdf_externally": True
                                                })

        for springer_books in range(407, len(self.urls)):
            books_downloaded = 0
            # Open Chrome...
            self.driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=chrome_options)

            # Open Springer Link Page
            self.driver.get(self.urls[springer_books])

            try:
                # Using Xpath
                try:
                    # Create the variable for the button to click - BE MINDFUL OF THE INTERNAL QUOTES / MAKE THEM SINGLE
                    self.search_button = self.driver.find_element_by_xpath("//*[@id='main-content']/article["
                                                                           "1]/div/div/div[ "
                                                                           "2]/div/div/a")
                    books_downloaded += 1
                    # Wait for the website to load
                    sleep(1)
                    self.search_button.click()
                    # Wait for download to complete...
                    self.download_wait("/home/frank/Documents/Springer_Books", 20)
                except:
                    self.search_button = self.driver.find_element_by_xpath("// *[ @ id = 'main-content'] / article[1] / "
                                                                           "div / div / div[2] / div[1] / a")
                    books_downloaded += 1
                    # Using CSS selector
                    # Create the variable for the button to click - BE MINDFUL OF THE INTERNAL QUOTES / MAKE THEM SINGLE
                    # self.search_button = self.driver.find_element_by_css_selector(
                    # "#main-content > article.main-wrapper.main-wrapper--no-gradient.main-wrapper--dual-main > div > div > "
                    # "div.cta-button-container.cta-button-container--stacked.u-pt-36 > div > div > a > svg")
                    # download_button.click()
                    # Wait for the website to load
                    sleep(1)
                    self.search_button.click()
                    # Wait for download to complete...
                    self.download_wait("/home/frank/Documents/Springer_Books", 20)

            except:

                print("Unable to download this book...")
                pass



            # Close current window
            self.driver.close()

            # Change to PDF page
            # self.driver.switch_to_window(self.driver.window_handles[1])

        self.driver.quit()


bot = PDFBot()
bot.get_hyperlinks_from_pdf()
bot.download_books()
