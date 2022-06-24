# Scraping data using Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
# CSV saver
from pandas import DataFrame
# for charging the config
from json import loads as JsonLoads
# using cmd and gettting file tree
from os.path import dirname as OsDirname, abspath as Osabspath, join as OsJoin, isfile as OsIsfile
from os import system as OsSystem, listdir as OsListdir


ROOT_DIR = OsDirname(Osabspath(__file__))  # Project Root

CONFIG_PATH = OsJoin(ROOT_DIR, 'configuration.conf')
# templates folder path
DIR_CONFIG_PATH = OsJoin(ROOT_DIR, r'templates\\')
# directory of the user for the chrome driver
DIR_CHROMEPROFIL_PATH = OsJoin(ROOT_DIR, r'driver\\driverProfile\\')
# folder where data are saved
DIR_SAVE_DATA_PATH = OsJoin(ROOT_DIR, r'data\\')
# path to have access to the chromedriver executable
DRIVER_PATH = OsJoin(ROOT_DIR, r'driver\\chromedriver.exe')

# TODO faire un installeur pour pouvoir save les variables global suivante dans un fichier
# directory of the chrome application where chrome.exe is located
DIR_CHROMEAPP_PATH = r'C:\\Program Files\\Google\\Chrome\\Application\\'
# port to use for the chrome debugger
PORT = 9222


def initChromeWindow():
    OsSystem(
        "cmd /k set PATH=%PATH%;%s" % DIR_CHROMEAPP_PATH)
    OsSystem(
        'cmd /k chrome.exe --remote-debugging-port=%d --user-data-dir=%s' % (PORT, DIR_CHROMEPROFIL_PATH))


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
    elements_table = [driver.find_elements(by=getByType(
        info["htmlTag"]), value=info["value"]) for info in config["savedInfos"]]
    return tuple(elements_table)


def modifyElement(config, elements_table, i, j):
    if(config["savedInfos"][i]["saveAsType"] == "string"):
        return elements_table[i][j].text
    elif(config["savedInfos"][i]["saveAsType"] == "link"):
        return elements_table[i][j].get_attribute("href")


def getElement(config, elements_table, i, j):
    try:
        return modifyElement(config, elements_table, i, j)
    except IndexError:
        print("Error while getting element")
        pass


def dictOfElements(config, elements_table, j):
    return {config["savedInfos"][i]["saveAs"]: getElement(config, elements_table, i, j) for i in range(len(config["savedInfos"]))}


def elementsToDataframe(config, elements_table):
    return DataFrame().from_records([dictOfElements(config, elements_table, j)
                                     for j in range(len(elements_table[0]))])


def getDataframe(driver, config):
    elements = getElements(driver, config)
    return elementsToDataframe(config, elements)


# TODO dont use concatenate with +
# TODO save depending on name or stuff like that so its easier to find
def saveDataframe(config, url, dataframe):
    try:
        folder_path = OsJoin(
            DIR_SAVE_DATA_PATH, config["csvSavedAs"] + "_" + url.split("?")[1] + ".csv")
        dataframe.to_csv(folder_path, index=False)
    except IndexError:
        folder_path = OsJoin(DIR_SAVE_DATA_PATH, config["csvSavedAs"] + ".csv")
        dataframe.to_csv(folder_path, index=False)
    finally:
        print("Data saved in " + folder_path)


# TODO faire une state machine pour pas charger le driver à chaque appuis du bouton ni meme la config
def main():

    # initChromeWindow()
    driver = setDriver()
    try:
        config = loadConfig(driver.current_url)
    except Exception as e:
        print(e)
        print("Cant load config")
        driver.close()
        exit(1)
    dataframe = getDataframe(driver, config)
    saveDataframe(config, driver.current_url, dataframe)


if __name__ == '__main__':
    main()
