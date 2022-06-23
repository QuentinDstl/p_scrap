import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# directory of the user for the chrome driver
DIR_CHROMEPROFIL_PATH = os.path.join(ROOT_DIR, r'driver\\driverProfile\\')
# TODO faire un installeur pour pouvoir save les variables global suivante dans un fichier
# directory of the chrome application where chrome.exe is located
DIR_CHROMEAPP_PATH = r'C:\\Program Files\\Google\\Chrome\\Application\\'
# port to use for the chrome debugger
PORT = 9222

# os.system(
#     'cmd /k "set PATH=%PATH%;%s"' % DIR_CHROMEAPP_PATH)
os.system(
    'cmd /k chrome.exe --remote-debugging-port=%d --user-data-dir=%s' % (PORT, DIR_CHROMEPROFIL_PATH))
