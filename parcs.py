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
from subprocess import Popen,CREATE_NEW_CONSOLE
# loading the environment variables
from dotenv import load_dotenv

#TODO remove
import time

load_dotenv()

ROOT_DIR = OsDirname(Osabspath(__file__))  # Project Root

# templates folder path
DIR_CONFIG_PATH = OsJoin(ROOT_DIR, 'templates\\')
# directory of the user for the chrome driver
DIR_CHROMEPROFIL_PATH = OsJoin(ROOT_DIR, 'driver\\driverProfile\\')
# path to have access to the chromedriver executable
DRIVER_PATH = OsJoin(ROOT_DIR, 'driver\\chromedriver.exe')


def initChromeWindow():
    prog_start = Popen(['cmd', '/c', 'set PATH=%%PATH%%;%s&&chrome.exe --remote-debugging-port=%s --user-data-dir=%s' % (OsGetenv('DIR_CHROMEAPP_PATH'), OsGetenv('PORT'), DIR_CHROMEPROFIL_PATH)], creationflags=CREATE_NEW_CONSOLE)    
    Popen('taskkill /F /PID %i' % prog_start.pid) #this will kill the invoked terminal 


def setDriver():
    # changing the options to open a debugger window that will be used to naviguate the browser
    # the new window is opened on the port 9222 of the localhost
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    try:
        driver = webdriver.Chrome(
            options=options, service=Service(DRIVER_PATH))
    except WebDriverException as e:
        print(e)
        print("Solution: Download on 'https://chromedriver.storage.googleapis.com/index.html' the latest version of the chromedriver and replace it in the 'driver' folder as 'chromedriver.exe'")
        exit(1)
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
    for filename in getFiles(DIR_CONFIG_PATH):
        short_filename = filename.split(".")[0]
        if short_filename in url:
            return filename
    return None


def loadJSON(filename):
    with open(DIR_CONFIG_PATH + filename) as json_file:
        return JsonLoads(json_file.read())


def getConfigFromRule(json, url):
    for rule in json["rules"]:
        if rule["differenceInUrl"] in url:
            return rule
    raise Exception("No rule found for this url")


def loadConfig(url):
    filename = isInConfigs(url)
    if(filename):
        json = loadJSON(filename)
        return getConfigFromRule(json, url)
    else:
        raise Exception("Config not found")


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


def getElement(config, elements_table, i, j):
    try:
        return modifyElement(config, elements_table, i, j)
    except IndexError as e:
        print(e)
        print(": Cant load element, check the missing information in the '.csv' file in 'data' folder and change the field 'value' corresponding in the '.json' file in the 'templates' folder ")
        pass


def createInformationDict(config, elements_table, j):
    return {config["savedInfos"][i]["saveAs"]: getElement(config, elements_table, i, j) for i, _ in enumerate(config["savedInfos"])}


def elementsToDataframe(config, elements_table):
    return DataFrame().from_records([createInformationDict(config, elements_table, j)
                                     for j, _ in enumerate(elements_table[0])])


def getDataframe(driver, config):
    elements = getElements(driver, config)
    return elementsToDataframe(config, elements)


def saveDataframe(config, url, dataframe):
    folder_path = OsJoin(
        OsGetenv('SAVE_DATA_PATH'), config["csvSavedBeginWith"] + url.split("/", 3)[3].replace("/", "%").replace("?", "@") + ".csv")
    dataframe.to_csv(folder_path, index=False)
    return folder_path


def main():
    initChromeWindow()
    driver = setDriver()
    print(driver.current_url)
    while 1:
        input("Press Enter to save current page")
        try:
            config = loadConfig(driver.current_url)
        except Exception as e:
            print(e)
            print("Cant load config")
            driver.close()
            exit(1)
        dataframe = getDataframe(driver, config)
        print(saveDataframe(config, driver.current_url, dataframe))


if __name__ == '__main__':
    main()
