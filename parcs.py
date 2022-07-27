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
from tkinter import Tk, Canvas, Text, Label, Button, PhotoImage, messagebox, Entry, filedialog, END
from tkinter.ttk import Scrollbar
# loading the environment variables
from dotenv import load_dotenv
from configparser import ConfigParser
from time import sleep
from threading import Thread
# slugify
from unicodedata import normalize
from re import sub

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

CONFIG_PATH = OsJoin(ROOT_DIR, '.config')


def load_config():
    config = ConfigParser()
    config.read(CONFIG_PATH)
    return config


def initConfig():
    config = load_config()
    global SAVE_DATA_PATH
    if(config.sections() == []):  # if the config is not found
        SAVE_DATA_PATH = ""
    else:
        SAVE_DATA_PATH = config["SAVING"]["SAVE_DATA_PATH"]


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
        messagebox.showerror("Chrome Error", "[#10]" + str(e))


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
        messagebox.showerror("Driver Error", "[#11]"+ str(e))
        messagebox.showinfo(
            "Driver Solution", "Download on 'https://chromedriver.storage.googleapis.com/index.html' the latest version of chromedriver and replace the previous 'chromedriver.exe' in the 'driver' folder")
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
    for page in json["pages"]:
        if page["urlSelector"] in url:
            return page
    raise Exception("[#22] No page found for %s" % url.split("/", 3)[2])


def loadConfig(url):
    filename = isInConfigs(url)
    if(filename):
        json = loadJSON(filename)
        return getConfigFromRule(json, url)
    else:
        raise Exception("[#23] Config not found for this %s" % url.split("/", 3)[2])


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
        raise Exception("[#24] Unknown html tag type %s" % html_type)


def getElements(driver, config):
    return tuple([driver.find_elements(by=getByType(
        info["htmlTag"]), value=info["value"]) for info in config["rules"]])


def modifyElement(config, elements_table, i, j):
    if(config["rules"][i]["saveType"] == "string"):
        return elements_table[i][j].text
    elif(config["rules"][i]["saveType"] == "link"):
        return elements_table[i][j].get_attribute("href")


def getElement(error_textbox, config, elements_table, i, j):
    try:
        return modifyElement(config, elements_table, i, j)
    except IndexError as e:
        guiPrint(error_textbox, "[#20] Cant load element, check the missing information in the '.csv' saved file and change the field 'value' or 'htmlTag' corresponding in the same template file")
        pass


def createInformationDict(error_textbox, config, elements_table, j):
    return {config["rules"][i]["saveAs"]: getElement(error_textbox, config, elements_table, i, j) for i, _ in enumerate(config["rules"])}


def elementsToDataframe(error_textbox, config, elements_table):
    return DataFrame().from_records([createInformationDict(error_textbox, config, elements_table, j)
                                     for j, _ in enumerate(elements_table[0])])


def getDataframe(driver, error_textbox, config):
    elements = getElements(driver, config)
    return elementsToDataframe(error_textbox, config, elements)


def saveDataframe(error_textbox, dataframe, saving_path):
    try:
        dataframe.to_csv(saving_path, index=False)
    except ImportError as e:
        guiPrint(error_textbox, "[#21] Name has special characters in it")
    return saving_path


def relativeToAssets(filename):
    return OsJoin(ASSETS_PATH, filename)


def setDriverToLast(driver):
    try:
        driver.switch_to.window(window_name=driver.window_handles[-1])
    except WebDriverException:
        exit(1)
    return driver


def openTemplatesFolder():
    Subrun([FILEBROWSER_PATH, DIR_TEMPLATES_PATH])


def toggleButtonSaving(button, saving, saving_image, base_image):
    if(saving):
        button.config(image=saving_image)
    else:
        button.config(image=base_image)


def saveDataPathToConfig():
    config = ConfigParser()
    config["SAVING"] = {}
    config["SAVING"]["SAVE_DATA_PATH"] = SAVE_DATA_PATH
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)


def setDataPath():
    saving_path = filedialog.askdirectory(
        initialdir=ROOT_DIR, title="Where to save ?")
    global SAVE_DATA_PATH
    SAVE_DATA_PATH = saving_path
    saveDataPathToConfig()


def slugify(text):
    text = str(text)
    text = normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = sub(r'[^\w\s-]', '', text.lower())
    return sub(r'[-\s]+', '-', text).strip('-_')


class AsyncScraper(Thread):
    def __init__(self, driver, error_textbox, saving_name):
        super().__init__()
        self.driver = driver
        self.error_textbox = error_textbox
        self.saving_name = slugify(saving_name)

    def run(self):
        try:
            config = loadConfig(driver.current_url)
        except Exception as e:
            guiPrint(self.error_textbox, e)
        else:
            dataframe = getDataframe(driver, self.error_textbox, config)
            if(self.saving_name == ""):
                self.saving_name = slugify(config["fileName"]) + self.driver.current_url.split(
                    "/", 3)[3].replace("/", "%").replace("?", "@")
            if(SAVE_DATA_PATH == ""):
                setDataPath()

            saving_path = OsJoin(SAVE_DATA_PATH,  self.saving_name + ".csv")
            guiPrint(self.error_textbox, "Data saved at: " +
                     saveDataframe(self.error_textbox, dataframe, saving_path))


class App(Tk):
    def __init__(self, driver):
        super().__init__()

        self.driver = driver
        self.geometry("282x240")
        self.iconbitmap(relativeToAssets("icon.ico"))
        self.title('Pinaack Webscraper')
        self.configure(bg="#FFFEFC")
        self.resizable(False, False)

        self.createBackground()
        self.createSaveButton()
        self.createPathSaveEntry()
        self.createSeeButton()
        self.createAddButton()
        self.createUiTerminal()

        self.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.buffer_windows_len = len(driver.window_handles)
        self.save_info.after(1000, self.parallelLoop)

    def createBackground(self):
        self.canvas = Canvas(
            self,
            bg="#FFFEFC",
            height=200,
            width=282,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(
            x=0,
            y=0
        )

    def monitor(self, thread):
        if thread.is_alive():
            self.after(200, lambda: self.monitor(thread))
        else:
            self.save_info.place(
                x=96.0,
                y=30.0
            )
            toggleButtonSaving(self.save_button, False,
                               self.saving_button_image, self.save_button_image)

    def getData(self):
        scraper_thread = AsyncScraper(
            self.driver, self.error_textbox, self.save_to_entry.get())
        scraper_thread.start()
        self.monitor(scraper_thread)

    def saveData(self, event):
        toggleButtonSaving(self.save_button, True,
                           self.saving_button_image, self.save_button_image)
        self.save_info.place_forget()  # delete error_textbox
        self.getData()

    def createSaveButton(self):
        self.saving_button_image = PhotoImage(
            file=relativeToAssets("saving_button.png"))
        self.save_button_image = PhotoImage(
            file=relativeToAssets("save_button.png"))
        self.save_button = Button(
            image=self.save_button_image,
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            command=lambda: self.saveData(None),
            relief="flat"
            # TODO delete saving animation without breaking design
            # relief="sunken"
        )
        self.save_button.place(
            x=20.0,
            y=20.0,
            width=242.0,
            height=40.0
        )
        self.save_info = Label(
            text=driver.title,
            anchor="nw",
            bg="#FD222B", fg="#FFFEFC",
            height="1", width="18",
            cursor="hand2",
            font=("Lato", 14 * -1)
        )
        self.save_info.place(
            x=96.0,
            y=30.0
        )
        self.save_info.bind("<Button-1>", self.saveData)

    def askSavingPath(self):
        setDataPath()

    def createPathSaveEntry(self):
        self.save_as_entry_image = PhotoImage(
            file=relativeToAssets("save_as_entry.png"))
        self.save_as_bg = self.canvas.create_image(
            122.0,
            90.0,
            image=self.save_as_entry_image
        )
        self.save_to_entry = Entry(
            bd=0,
            bg="#ECECEC",
            highlightthickness=0
        )
        self.save_to_entry.place(
            x=48.0,
            y=81.0,
            width=172.0,
            height=18.0
        )
        self.save_in_button_image = PhotoImage(
            file=relativeToAssets("save_in_button.png"))
        self.save_in_button = Button(
            image=self.save_in_button_image,
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            command=lambda: self.askSavingPath(),
            relief="flat"
        )
        self.save_in_button.place(
            x=224.0,
            y=80.0,
            width=38.0,
            height=20.0
        )

    def createSeeButton(self):
        self.see_button_image = PhotoImage(
            file=relativeToAssets("see_button.png"))
        self.see_button = Button(
            image=self.see_button_image,
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            command=lambda: openTemplatesFolder(),
            relief="flat"
        )
        self.see_button.place(
            x=20.0,
            y=114.0,
            width=113.0,
            height=20.0
        )

    def createAddButton(self):
        self.add_button_image = PhotoImage(
            file=relativeToAssets("add_button.png"))
        self.add_button = Button(
            image=self.add_button_image,
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            command=lambda: guiPrint(
                self.error_textbox, "This function is not working for the moment"),
            relief="flat"
        )
        self.add_button.place(
            x=153.0,
            y=114.0,
            width=109.0,
            height=20.0
        )

    def createUiTerminal(self):
        self.error_textbox = Text(
            self, wrap="word",
            state="disabled",
            bg="#ECECEC", bd=0,
            width=27, height=4,
            padx=4, pady=4,
        )
        self.error_textbox.place(
            x=21.0,
            y=151.0
        )
        scrollbar = Scrollbar(
            self,
            orient='vertical',
            command=self.error_textbox.yview
        )
        scrollbar.place(
            x=246.0,
            y=151.0,
            height=72.0
        )
        self.error_textbox['yscrollcommand'] = scrollbar.set
        self.cls_button_image = PhotoImage(
            file=relativeToAssets("cls_button.png"))
        self.cls_button = Button(
            image=self.cls_button_image,
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            command=lambda: guiCls(self.error_textbox),
            relief="flat"
        )
        self.cls_button.place(
            x=226.0,
            y=202.0,
            width=19.0,
            height=19.0
        )
        guiPrint(self.error_textbox,
                 "This is a scrollable window to display error messages. To clean up messages click on the cross ->")

    def onClosing(self):
        try:
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                self.driver.close()
            self.driver.quit()
        except Exception:
            pass
        finally:
            self.destroy()

    def parallelLoop(self):
        if(self.buffer_windows_len != len(self.driver.window_handles)):
            self.buffer_windows_len = len(self.driver.window_handles)
            self.driver = setDriverToLast(self.driver)
        self.save_info.configure(text=self.driver.title)
        self.after(200, self.parallelLoop)


if __name__ == '__main__':
    initConfig()
    if(SAVE_DATA_PATH == ""):
        setDataPath()
    initChromeWindow()
    driver = setDriver()
    app = App(driver)
    app.mainloop()
