## tuto 
https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/#launch-browser-with-custom-flags

## what have been done to launch project
add chrome.exe in %PATH% of windows environment variable
pip install all the requirements in requirements.txt
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeScraperProfile"
    - For --remote-debugging-port value you can specify any port that is open.
    - For --user-data-dir flag you need to pass a directory where a new Chrome profile will be created

## TODO V2
SPEED :
use pypy3
use numpy for matrix and use jit on top of it

http://sdz.tdct.org/sdz/creer-une-installation.html

## TODO V1
definir la basic rule -> attention doit etre placé en dernier sinon ca casse tout
voir pour les profil linkedin pour prendre les sections mais voir comment faire

TEST de debugging :
raise toutes les erreurs possible
do all the test to see if everything is secured and safe
no windows init.py -> freeze : check si le driver est toujours on

# IHM PATH

launch parcs.exe
    a window open :cd De  
    button start -> launch browser
        then you can :
            save the page with a button
            see templates that exist 
            add a templates