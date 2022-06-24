from os.path import dirname as OsDirname, abspath as Osabspath, join as OsJoin
from os import system as OsSystem, getenv as OsGetenv
# loading the environment variables
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = OsDirname(Osabspath(__file__))  # Project Root
# directory of the user for the chrome driver
DIR_CHROMEPROFIL_PATH = OsJoin(ROOT_DIR, r'driver\\driverProfile\\')


# def initChromeWindow():
#     OsSystem(
#         "cmd /k set PATH=%PATH%;%s" % OsGetenv('DIR_CHROMEAPP_PATH'))
#     OsSystem(
#         'cmd /k chrome.exe --remote-debugging-port=%d --user-data-dir=%s' % (OsGetenv('PORT'), DIR_CHROMEPROFIL_PATH))

OsSystem(
    'cmd /k chrome.exe --remote-debugging-port=%d --user-data-dir=%s' % (OsGetenv('PORT'), DIR_CHROMEPROFIL_PATH))
