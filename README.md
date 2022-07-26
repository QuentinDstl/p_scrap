<p align="center">
  <img src="https://media-exp1.licdn.com/dms/image/C4E0BAQFJMuP43XCVKQ/company-logo_200_200/0/1620734759790?e=2147483647&v=beta&t=f6EcoAHEsKWQqcbJ6JMyPwGkhQgsKUfDxF9VVpA6ufo" width="100" />
  <h1 align="center">Pinaack Webscraper</h1>
</p>

Installation
============

You need to clone the repo at this [link](https://github.com/QuentinDstl/p_scarp) or download the zip file.

__You may need to change manually some stuff in some of the following files:__

.config file
------------

| what is in `.config` |||
|---|---|---|
| `[SAVING] SAVE_DATA_PATH` | _C:/Folder/To/Save/the_result.csv_ | 💾 where to save the current website |

> ⚠️ If `.config` dont exist it will be created on next launch and you will be asked to chose it.


.env file
---------

| what is in `.env` |||
|---|---|---|
| `DIR_CHROMEAPP_PATH` | _C:/Program Files/Google/Chrome/Application/_ | 📁 use to launch Chrome on debugging mode |
| `PORT` | _9222_ | 🔌port use to launch the new chrome window |

> ⚠️ The `PORT` must __not be used by another app__. Launch `cmd` with admin rights and execute : `netstat -a` to see what port are used.

> ⚠️ To get the `DIR_CHROMEAPP_PATH` :
> ```
> 1. Window + S: to start a research
> 2. now search for `Chrome`
> 3. righ-click on the logo that just pop
> 4. click on: Open File Location
> 5. in the new window, right-click on `Google Chrome` shortcut file
> 6. click on: Open File Location
> 7. copy paste the path of the newly opened folder into the `.env` file
> ```
> The __path should look like__ that : `C:/Files/Chrome/Application/`.

Features
========
Templates
---------

Templates are used to know what to scrape on what website. 
 You can find in `example.json` an example of a set of rules and template information.
 
 A template have 2 important parts:
  1. The Template Specific Name
  2. The Template List of Rules
     - A. The Rule Guideline
     - B. The Rule Saving Informations
     - C. The Basic Rule (_optional_)

<br>

### __1. Template specific Name__

The __name__ of the template file : `name.json` is important as it will be the string used to load it.

> ⚠️ If you want to scrap data on the website `https://www.scrap-me.com`, you will need to create a `scrap-me.json` file.

<br>

### __2. The Template List of Rules__

You will find in the template a `"rules"` array that contain all the individual rule in some `{}` and separate by `,`.


### _A. The Rule Guideline_

A rule start with two values:
  1. The __selector__ of the element to scrap
  2. The __attribute__ of the element to scrap
"csvSavedBeginWith": "LinkdinProfile", -> savedAs
            "differenceInUrl": "/", -> urlSelector
            rules -> pages
            savedInfos -> rules

### _B. The Rule Saving Informations_

<ins>example.json :</ins>
```json
{
    "rules": [
        {
            💬 this is the name use for the default saved csv
            "csvSavedBeginWith": "Name_for_my_csv",
            💬 this is a string that will be use to differentiate pages of a website
            "differenceInUrl": "/particular_path_in_url/",
            💬 this is the informations you want to save, you can add more then 4
            "savedInfos": [
                {
                    💬 this is what the selenium will search for, here it's: class="companies"
                    "htmlTag": "class",
                    "value": "companies",
                    💬 this is the name of the column in the csv
                    "saveAs": "Company Name",
                    💬 this is the format of the saved information
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

```python
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
```

### _The basic rule_

by using `"/"` as the selector to differentiate between all the link of a same website :
```"differenceInUrl": "/",```
you will create a set of rules that will work on any page of the website (because every `url` have the `/` charactère in it). This mean that __it's very important to put this rule at the bottom end of the list__ so it will be the last one to be applied if any other rule match.




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

----------------------------------------------------------------
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
