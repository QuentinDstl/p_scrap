<p align="center">
  <img src="https://media-exp1.licdn.com/dms/image/C4E0BAQFJMuP43XCVKQ/company-logo_200_200/0/1620734759790?e=2147483647&v=beta&t=f6EcoAHEsKWQqcbJ6JMyPwGkhQgsKUfDxF9VVpA6ufo" width="100" />
  <h1 align="center">Pinaack Webscraper</h1>
</p>

Installation
============

You need to clone the repo at this [link](https://github.com/QuentinDstl/p_scarp) or download the zip file.

__You may need to change manually some stuff in some of the following files:__

.config file
---------

| what is in `.config` |||
|---|---|---|
| `[SAVING] SAVE_DATA_PATH` | C:/Folder/To/Save/the_result.csv | 💾 where to save the current website |

> ⚠️ If `.config` dont exist it will be created on next launch and you will be asked to chose it


.env file
---------

| what is in `.env` |||
|---|---|---|
| `DIR_CHROMEAPP_PATH` | C:/Program Files/Google/Chrome/Application/ | 📁 use to launch Chrome on debugging mode |
| `PORT` | 9222 | 🔌port use to launch the new chrome window |

> ⚠️ The `PORT` must not be used by another app. Launch `cmd` with admin rights and execute : `netstat -a` to see what port are used.

> ⚠️ To get the `DIR_CHROMEAPP_PATH` :
> ```
> 1. Window + S: to start a research
> 2. now search for `Chrome`
> 3. righ-click on the logo that just pop
> 4. click on: Open File Location
> 5. in the new window, right-click on `Google Chrome` shortcut file
> 6. click on: Open File Location
> 7. select the path of the newly opened folder
> ```

Features
========
Templates
---------

Templates are used to know what to scrape on what website. 

### 📕 _How template work ?_

here is `example.json` where you can fin an example of a set of rules. The name of the `.json` is it important as it will be the string used to load it.
```json
{
    "rules": [
        {
            this is the name use for the default saved csv
            "csvSavedBeginWith": "Name_for_my_csv",
            this is a string that will be use to differentiate pages of a website
            "differenceInUrl": "/particular_path_in_url/",
            this is the informations you want to save, you can add more then 4
            "savedInfos": [
                {
                    "htmlTag": "class",
                    "value": "companies",
                    "saveAs": "Company Name",
                    "saveAsType": "string"
                },
                {
                    "htmlTag": "id",
                    "value": "the-title-id",
                    "saveAs": "Title",
                    "saveAsType": "string"
                },
                {
                    "htmlTag": "xpath",
                    "value": "//section/dl/dd[2]",
                    "saveAs": "Informations",
                    "saveAsType": "string"
                },
                {
                    "htmlTag": "xpath",
                    "value": "//section/dl/dd[2]/a/span",
                    "saveAs": "Website",
                    "saveAsType": "link"
                }
            ]
        }
    ]
}
```

### ❓ _How to ceate a template ?_

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

### ❗ _The basic rule_

by using `"/"` as the selector to differentiate between the differents link of a website :
```"differenceInUrl": "/",```
you will create some rule for any page of the website, because every `url` have this char in it ... so **this is very important to put this rule at the bottom end of the list** so it will be the last one to be applied if any other rule match.




Error Message Box
=================



How everything works together
=============================

```bash
├── assets
│   └── ...     # all .png and .ico for the design are there
├── driver
│   ├── driverProfile
│   │   └── ... # all stuff from Google are there
│   └── chromedriver.exe
├── templates
│   └── ...     # templates for scraping data from website
├── .config     # file with user configuration 
├── .env        # file with general configuration
└───.gitignore
```

## what have been done to launch projecte
pip install all the requirements in requirements.txt

https://nuitka.net/doc/user-manual.html

## TODO V2
SPEED :
use pypy3
use numpy for matrix and use jit on top of it

http://sdz.tdct.org/sdz/creer-une-installation.html

## TODO V1
raise toutes les erreurs possible
do all the test to see if everything is secured and 
