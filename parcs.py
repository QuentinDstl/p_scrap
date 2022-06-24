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
from os.path import dirname as OsDirname, abspath as Osabspath, join as OsJoin, isfile as OsIsfile, isdir as OsIsdir, normpath as OsNormpath
from os import listdir as OsListdir, getenv as OsGetenv
# execute command in a shell to open a browser
from subprocess import Popen, CREATE_NEW_CONSOLE, run as Subrun
# GUI
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
# loading the environment variables
from dotenv import load_dotenv

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


def initChromeWindow():
    prog_start = Popen(['cmd', '/c', 'set PATH=%%PATH%%;%s&&chrome.exe --remote-debugging-port=%s --user-data-dir=%s' %
                       (OsGetenv('DIR_CHROMEAPP_PATH'), OsGetenv('PORT'), DIR_CHROMEPROFIL_PATH)], creationflags=CREATE_NEW_CONSOLE)
    # this will kill the invoked terminal
    Popen('taskkill /F /PID %i' % prog_start.pid)


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

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def getData(driver):
    try:
        config = loadConfig(driver.current_url)
    except Exception as e:
        print(e)
    else:
        dataframe = getDataframe(driver, config)
        print(saveDataframe(config, driver.current_url, dataframe))


def openTemplatesFolder():
    Subrun([FILEBROWSER_PATH, DIR_TEMPLATES_PATH])


def createTkWindow(driver):
    window = Tk()

    window.geometry("300x200")
    window.configure(bg="#FFFEFC")

    canvas = Canvas(
        window,
        bg="#FFFEFC",
        height=200,
        width=300,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)
    background_image = PhotoImage(
        file=relative_to_assets("background.png"))
    background = canvas.create_image(
        75.0,
        100.0,
        image=background_image
    )
    add_button_image = PhotoImage(
        file=relative_to_assets("add_button.png"))
    add_button = Button(
        image=add_button_image,
        borderwidth=0,
        highlightthickness=0,
        command = lambda: print("add_button clicked"),
        # command=getData(driver),
        relief="flat"
    )
    add_button.place(
        x=171.0,
        y=97.0,
        width=109.0,
        height=20.0
    )
    see_button_image = PhotoImage(
        file=relative_to_assets("see_button.png"))
    see_button = Button(
        image=see_button_image,
        borderwidth=0,
        highlightthickness=0,
        command = lambda: print("see_button clicked"),
        # command=openTemplatesFolder(),
        relief="flat"
    )
    see_button.place(
        x=170.0,
        y=68.0,
        width=113.0,
        height=20.0
    )
    save_button_image = PhotoImage(
        file=relative_to_assets("save_button.png"))
    save_button = Button(
        image=save_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("save_button clicked"),
        relief="flat"
    )
    save_button.place(
        x=170.0,
        y=20.0,
        width=110.0,
        height=40.0
    )
    canvas.create_text(
        14.0,
        8.0,
        anchor="nw",
        text="How to use it ?",
        fill="#FFFEFC",
        font=("Lato Bold", 15 * -1)
    )
    canvas.create_text(
        14.0,
        65.0,
        anchor="nw",
        text="Go to a webpage",
        fill="#FFFEFC",
        font=("Lato", 15 * -1)
    )
    canvas.create_text(
        14.0,
        119.0,
        anchor="nw",
        text="template exist it",
        fill="#FFFEFC",
        font=("Lato", 15 * -1)
    )
    canvas.create_text(
        14.0,
        137.0,
        anchor="nw",
        text="will be save, else",
        fill="#FFFEFC",
        font=("Lato", 15 * -1)
    )
    canvas.create_text(
        14.0,
        155.0,
        anchor="nw",
        text="add yourself a new",
        fill="#FFFEFC",
        font=("Lato", 15 * -1)
    )
    canvas.create_text(
        14.0,
        173.0,
        anchor="nw",
        text="one",
        fill="#FFFEFC",
        font=("Lato", 15 * -1)
    )
    canvas.create_text(
        14.0,
        29.0,
        anchor="nw",
        text="Go to the new",
        fill="#FFFEFC",
        font=("Lato", 15 * -1)
    )
    canvas.create_text(
        14.0,
        47.0,
        anchor="nw",
        text="opened browser",
        fill="#FFFEFC",
        font=("Lato", 15 * -1)
    )
    canvas.create_text(
        14.0,
        83.0,
        anchor="nw",
        text="and click on save",
        fill="#FFFEFC",
        font=("Lato", 15 * -1)
    )
    canvas.create_text(
        14.0,
        101.0,
        anchor="nw",
        text="Data, if a related",
        fill="#FFFEFC",
        font=("Lato", 15 * -1)
    )
    canvas.create_rectangle(
        160.0,
        130.0,
        290.0,
        190.0,
        fill="#D9D9D9",
        outline="")
    window.resizable(False, False)
    window.mainloop()


def main():
    initChromeWindow()
    driver = setDriver()
    createTkWindow(driver)


if __name__ == '__main__':
    main()
