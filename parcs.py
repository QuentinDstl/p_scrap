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
# GUI
from tkinter import Tk, Canvas, Text, Button, PhotoImage, messagebox, END
from tkinter.ttk import Scrollbar
# loading the environment variables
from dotenv import load_dotenv
from time import sleep

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


def guiPrint(label, message):
    label.configure(state="normal")
    label.insert(END, str(message))
    label.insert(END, "\n\n")
    label.configure(state="disabled")


def guiCls(label):
    label.configure(state="normal")
    label.delete(1.0, END)
    label.configure(state="disabled")


def initChromeWindow():
    try:
        prog_start = Popen(['cmd', '/c', 'set PATH=%%PATH%%;%s&&chrome.exe --remote-debugging-port=%s --user-data-dir=%s' %
                            (OsGetenv('DIR_CHROMEAPP_PATH'), OsGetenv('PORT'), DIR_CHROMEPROFIL_PATH)], creationflags=CREATE_NEW_CONSOLE)
        sleep(1)
        prog_start.kill()
    except Exception as e:
        messagebox.showerror("Chrome Error", str(e))


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


def getElement(label, config, elements_table, i, j):
    try:
        return modifyElement(config, elements_table, i, j)
    except IndexError as e:
        guiPrint(label, ": Cant load element, check the missing information in the '.csv' file in 'data' folder and change the field 'value' corresponding in the '.json' file in the 'templates' folder ")
        pass


def createInformationDict(label, config, elements_table, j):
    return {config["savedInfos"][i]["saveAs"]: getElement(label, config, elements_table, i, j) for i, _ in enumerate(config["savedInfos"])}


def elementsToDataframe(label, config, elements_table):
    return DataFrame().from_records([createInformationDict(label, config, elements_table, j)
                                     for j, _ in enumerate(elements_table[0])])


def getDataframe(driver, label, config):
    elements = getElements(driver, config)
    return elementsToDataframe(label, config, elements)


def saveDataframe(config, url, dataframe):
    folder_path = OsJoin(
        OsGetenv('SAVE_DATA_PATH'), config["csvSavedBeginWith"] + url.split("/", 3)[3].replace("/", "%").replace("?", "@") + ".csv")
    dataframe.to_csv(folder_path, index=False)
    return folder_path


def relativeToAssets(filename):
    return OsJoin(ASSETS_PATH, filename)


def getDriverLastWindow(driver):
    if (len(driver.window_handles) != 1):
        driver.switch_to.window(window_name=driver.window_handles[-1])
    return driver


def getData(driver, label):
    driver = getDriverLastWindow(driver)
    try:
        config = loadConfig(driver.current_url)
    except Exception as e:
        guiPrint(label, e)
    else:
        dataframe = getDataframe(driver, label, config)
        guiPrint(label, "Data saved: " +
                 saveDataframe(config, driver.current_url, dataframe))


def openTemplatesFolder():
    Subrun([FILEBROWSER_PATH, DIR_TEMPLATES_PATH])


def main(driver):
    window = Tk()

    window.geometry("432x200")
    window.title('Pinaack Website Saver')
    window.configure(bg="#FFFEFC")

    canvas = Canvas(
        window,
        bg="#FFFEFC",
        height=200, width=432,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)
    background_image = PhotoImage(
        file=relativeToAssets("background.png"))
    canvas.create_image(
        75.0, 100.0,
        image=background_image
    )
    add_button_image = PhotoImage(
        file=relativeToAssets("add_button.png"))
    add_button = Button(
        image=add_button_image,
        borderwidth=0,
        highlightthickness=0,
        cursor="hand2",
        command=lambda: guiPrint(
            label, "This function is not working for the moment"),
        relief="flat"
    )
    add_button.place(
        x=303.0, y=74.0, width=109.0, height=20.0
    )
    see_button_image = PhotoImage(
        file=relativeToAssets("see_button.png"))
    see_button = Button(
        image=see_button_image,
        borderwidth=0,
        highlightthickness=0,
        cursor="hand2",
        command=lambda: openTemplatesFolder(),
        relief="flat"
    )
    see_button.place(
        x=170.0, y=74.0, width=113.0, height=20.0
    )
    save_button_image = PhotoImage(
        file=relativeToAssets("save_button.png"))
    save_button = Button(
        image=save_button_image,
        borderwidth=0,
        highlightthickness=0,
        cursor="hand2",
        command=lambda: getData(driver, label),
        relief="flat"
    )
    save_button.place(
        x=170.0, y=20.0, width=242.0, height=40.0
    )
    canvas.create_text(
        14.0, 8.0,
        anchor="nw",
        text="How to use it ?",
        fill="#FFFEFC",
        font=("Lato Bold", 15 * -1)
    )
    canvas.create_text(
        14.0, 29.0,
        anchor="nw",
        text=TUTO_MESSAGE,
        fill="#FFFEFC",
        font=("Lato", 15 * -1)
    )
    label = Text(
        window, wrap="word",
        state="disabled",
        bg="#ECECEC", bd=0,
        width=27, height=4,
        padx=4, pady=4,
    )
    label.place(x=171.0, y=111.0)
    scrollbar = Scrollbar(window, orient='vertical', command=label.yview)
    scrollbar.place(x=396.0, y=111.0, height=72.0)
    label['yscrollcommand'] = scrollbar.set

    cls_button_image = PhotoImage(
        file=relativeToAssets("cls_button.png"))
    cls_button = Button(
        image=cls_button_image,
        borderwidth=0,
        highlightthickness=0,
        cursor="hand2",
        command=lambda: guiCls(label),
        relief="flat"
    )
    cls_button.place(x=376.0, y=162.0, width=19.0, height=19.0)

    window.resizable(False, False)
    guiPrint(label, "This is a scrollable window to display error messages. To clean up messages click on the cross ->")

    def onClosing():
        try:
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                driver.close()
            driver.quit()
        except Exception:
            pass
        finally:
            window.destroy()
   
    window.protocol("WM_DELETE_WINDOW", onClosing)
    window.mainloop()


if __name__ == '__main__':
    # setup
    initChromeWindow()
    driver = setDriver()
    # main
    main(driver)
