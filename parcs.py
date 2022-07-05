# Scraping data using Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
# CSV saver
from pandas import DataFrame
# for charging the config
from json import loads as JsonLoads
# charge the templates and see templates files
from os.path import dirname as OsDirname, abspath as Osabspath, join as OsJoin, isfile as OsIsfile
from os import listdir as OsListdir, getenv as OsGetenv
# execute command in a shell to open a browser
from subprocess import Popen, CREATE_NEW_CONSOLE, run as Subrun
# using tkinter to create the gui of the project
from tkinter import Tk, Canvas, Text, Label, Button, PhotoImage, messagebox, END
from tkinter.ttk import Scrollbar
# loading the environment variables
from dotenv import load_dotenv
from time import sleep
from threading import Thread

load_dotenv()

ROOT_DIR = OsDirname(Osabspath(__file__))  # Project Root

# templates folder path
DIR_TEMPLATES_PATH = OsJoin(ROOT_DIR, 'templates\\')
# directory of the user for the chrome driver
DIR_CHROMEPROFIL_PATH = OsJoin(ROOT_DIR, 'driver\\driverProfile\\')
# path to have access to the chromedriver executable
DRIVER_PATH = OsJoin(ROOT_DIR, 'driver\\chromedriver.exe')
# path to assets folder for the GUI
ASSETS_PATH = OsJoin(ROOT_DIR, 'assets\\')
# path to open explorer.exe
FILEBROWSER_PATH = OsJoin(OsGetenv('WINDIR'), 'explorer.exe')

# tutorial message to show the user how to use the program
TUTO_MESSAGE = "Go to a webpage\non the new opened\nbrowser. Click on\n'Save Data' to save\nthe lastest opened\ntab. If a related \ntemplate exist it will\nbe save, else add\nyourself a new one"


def guiPrint(error_textbox, message):
    error_textbox.configure(state="normal")
    error_textbox.insert(1.0, "\n\n")
    error_textbox.insert(1.0, str(message))
    error_textbox.configure(state="disabled")


def guiCls(error_textbox):
    error_textbox.configure(state="normal")
    error_textbox.delete(1.0, END)
    error_textbox.configure(state="disabled")


"""
---------------------------------------------------- Open Browser ----------------------------------------------------
"""


def initChromeWindow():
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeScraperProfile"
    # ---> for --remote-debugging-port value you can specify any port that is open.
    # ---> for --user-data-dir flag you need to pass a directory where a new Chrome profile will be created
    try:
        prog_start = Popen(['cmd', '/c', 'set PATH=%%PATH%%;%s&&chrome.exe --remote-debugging-port=%s --user-data-dir=%s' %
                            (OsGetenv('DIR_CHROMEAPP_PATH'), OsGetenv('PORT'), DIR_CHROMEPROFIL_PATH)], creationflags=CREATE_NEW_CONSOLE)
        sleep(1)
        prog_start.kill()
    except Exception as e:
        messagebox.showerror("Chrome Error", str(e))


"""
---------------------------------------------------- Set Driver ----------------------------------------------------
"""


def setDriver():
    # changing the options to open a debugger window that will be used to naviguate the browser
    # the new window is opened on the port 9222 of the localhost
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    try:
        driver = webdriver.Chrome(
            options=options, service=Service(DRIVER_PATH))
    except WebDriverException as e:
        messagebox.showerror("Driver Error", str(e))
        messagebox.showinfo(
            "Driver Solution", "Download on 'https://chromedriver.storage.googleapis.com/index.html' the latest version of the chromedriver and replace it in the 'driver' folder as 'chromedriver.exe'")
    return driver


def getFiles(folder_path):
    for file in OsListdir(folder_path):
        if OsIsfile(OsJoin(folder_path, file)):
            yield file


# this way around is slower then looking from the url split
# into file because whe could use the fact that file are
# ordered but its more flexible because if the url name is
# app.something.net it wont be found
def isInConfigs(url):
    for filename in getFiles(DIR_TEMPLATES_PATH):
        short_filename = filename.split(".")[0]
        if short_filename in url:
            return filename
    return None


def loadJSON(filename):
    with open(DIR_TEMPLATES_PATH + filename) as json_file:
        return JsonLoads(json_file.read())


def getConfigFromRule(json, url):
    for rule in json["rules"]:
        if rule["differenceInUrl"] in url:
            return rule
    raise Exception("No rule found for %s" % url.split("/", 3)[2])


def loadConfig(url):
    filename = isInConfigs(url)
    if(filename):
        json = loadJSON(filename)
        return getConfigFromRule(json, url)
    else:
        raise Exception("Config not found for this %s" % url.split("/", 3)[2])


def getByType(html_type):
    if(html_type == "class"):
        return By.CLASS_NAME
    elif(html_type == "id"):
        return By.ID
    elif(html_type == "tag"):
        return By.TAG_NAME
    elif(html_type == "name"):
        return By.NAME
    elif(html_type == "link"):
        return By.LINK_TEXT
    elif(html_type == "partialLink"):
        return By.PARTIAL_LINK_TEXT
    elif(html_type == "css"):
        return By.CSS_SELECTOR
    elif(html_type == "xpath"):
        return By.XPATH
    else:
        raise Exception("Unknown html type")


def getElements(driver, config):
    return tuple([driver.find_elements(by=getByType(
        info["htmlTag"]), value=info["value"]) for info in config["savedInfos"]])


def modifyElement(config, elements_table, i, j):
    if(config["savedInfos"][i]["saveAsType"] == "string"):
        return elements_table[i][j].text
    elif(config["savedInfos"][i]["saveAsType"] == "link"):
        return elements_table[i][j].get_attribute("href")


def getElement(error_textbox, config, elements_table, i, j):
    try:
        return modifyElement(config, elements_table, i, j)
    except IndexError as e:
        guiPrint(error_textbox, ": Cant load element, check the missing information in the '.csv' file in 'data' folder and change the field 'value' corresponding in the '.json' file in the 'templates' folder ")
        pass


def createInformationDict(error_textbox, config, elements_table, j):
    return {config["savedInfos"][i]["saveAs"]: getElement(error_textbox, config, elements_table, i, j) for i, _ in enumerate(config["savedInfos"])}


def elementsToDataframe(error_textbox, config, elements_table):
    return DataFrame().from_records([createInformationDict(error_textbox, config, elements_table, j)
                                     for j, _ in enumerate(elements_table[0])])


def getDataframe(driver, error_textbox, config):
    elements = getElements(driver, config)
    return elementsToDataframe(error_textbox, config, elements)


def saveDataframe(config, url, dataframe):
    folder_path = OsJoin(
        OsGetenv('SAVE_DATA_PATH'), config["csvSavedBeginWith"] + url.split("/", 3)[3].replace("/", "%").replace("?", "@") + ".csv")
    dataframe.to_csv(folder_path, index=False)
    return folder_path


def relativeToAssets(filename):
    return OsJoin(ASSETS_PATH, filename)


def setDriverToLast(driver):
    try:
        driver.switch_to.window(window_name=driver.window_handles[-1])
    except WebDriverException:
        exit(1)
    return driver


"""
def getData(driver, error_textbox, save_info, save_button, saving_button_image, save_button_image):
    try:
        config = loadConfig(driver.current_url)
    except Exception as e:
        guiPrint(error_textbox, e)
    else:
        dataframe = getDataframe(driver, error_textbox, config)
        guiPrint(error_textbox, "Data saved: " +
                 saveDataframe(config, driver.current_url, dataframe))
    finally:
        save_info.place(x=246.0, y=30.0)
        toggleButtonSaving(save_button, False,
                           saving_button_image, save_button_image)
"""


def openTemplatesFolder():
    Subrun([FILEBROWSER_PATH, DIR_TEMPLATES_PATH])


def toggleButtonSaving(button, saving, saving_image, base_image):
    if(saving):
        button.config(image=saving_image)
    else:
        button.config(image=base_image)


class AsyncScraper(Thread):
    def __init__(self, driver, error_textbox):
        super().__init__()
        self.driver = driver
        self.error_textbox = error_textbox
    def run(self):
        try:
            config = loadConfig(driver.current_url)
        except Exception as e:
            guiPrint(self.error_textbox, e)
        else:
            dataframe = getDataframe(self.driver, self.label, config)
            guiPrint(self.label, "Data saved: " +
                    saveDataframe(config, self.driver.current_url, dataframe))


    def monitor(self, thread):
        if thread.is_alive():
            self.after(200, lambda: self.monitor(thread))
        else:
            self.save_info.place(x=246.0, y=30.0)
            toggleButtonSaving(self.save_button, False,
                               self.saving_button_image, self.save_button_image)
        try:
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                driver.close()
            driver.quit()
        except Exception:
            pass
        finally:
            window.destroy()

    buffer_windows_len = len(driver.window_handles)

    def parallelLoop():
        nonlocal buffer_windows_len
        nonlocal driver
        if(buffer_windows_len != len(driver.window_handles)):
            buffer_windows_len = len(driver.window_handles)
            driver = setDriverToLast(driver)
        save_info.configure(text=driver.title)
        window.after(200, parallelLoop)

    window.protocol("WM_DELETE_WINDOW", onClosing)
    save_info.after(1000, parallelLoop)
    window.mainloop()


if __name__ == '__main__':
    # setup
    initChromeWindow()
    driver = setDriver()
    # main
    main(driver)
