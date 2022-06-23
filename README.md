# TODO

## tuto 
https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/#launch-browser-with-custom-flags

## ce qui a été fait
ajouter chrome.exe dans les %PATH%
lancer chrome avec des options
pip install selenium, pandas, xlwt
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeScraperProfile"
    - For --remote-debugging-port value you can specify any port that is open.
    - For --user-data-dir flag you need to pass a directory where a new Chrome profile will be created
  
il faut définir le chromedriver.exe


## TODO
SPEED :
use pypy3
https://www.loginradius.com/blog/engineering/speed-up-python-code/
- use tuple instead of list for the data (but tupple is immutable)
- Use list comprehension
- Use generators

http://sdz.tdct.org/sdz/creer-une-installation.html

faire une serie de test avec des trucs en moins et voir pour blinder
attention : si y'a pas de fenetre = freeze
quand il y'a pas de model

# IHM PATH

lancer parcs.exe
    ouvre une fenetre avec :
    bouton start -> lance le navigateur
        une fois que c'est start on a :
            bouton pour save
            link pour voir les models
            link pour ajouter un model