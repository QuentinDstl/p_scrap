from os.path import dirname as OsDirname, abspath as Osabspath, join as OsJoin
from os import system as OsSystem, getenv as OsGetenv
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = OsDirname(Osabspath(__file__))
DIR_CHROMEPROFIL_PATH = OsJoin(ROOT_DIR, r'driver\\driverProfile\\')

OsSystem(
    'cmd /k "set PATH=%%PATH%%;%s&&chrome.exe --remote-debugging-port=%s --user-data-dir=%s"' % (OsGetenv('DIR_CHROMEAPP_PATH'), OsGetenv('PORT'), DIR_CHROMEPROFIL_PATH))
