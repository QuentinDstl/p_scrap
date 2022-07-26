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

> 📖 To get the `DIR_CHROMEAPP_PATH` :
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

------------------------------------------------------------

<br>

Features
========
Templates
---------

Templates are used to know what information to scrape on what website. 
 You can find in `example.json` an example of a set of pages and rules.
 
 A template have 2 important parts:
  1. The Template Specific Name
  2. The Template List of Pages
     - A. The Page Guideline
     - B. The Page Rules
     - C. The Page Basic Rule (_optional_)

<br>

### ___1. Template Specific Name___

The __name__ of the template file : `name.json` is important as it will be the string used to load it.

> 📖 For exemple, if you want to scrap data on the website `https://www.scrap-me.com`, you will need to create a `scrap-me.json` template file.

<br>

### ___2. The Template List of pages___

A website can have many diffent pages. For exemple `https://www.scrap-me.com` can have the following pages :
- `https://www.scrap-me.com/profiles`
- `https://www.scrap-me.com/companies`

We can create different scrapping rules for each one of them or create a basic rule that will apply on every page.

You will find in the template a `"pages"` array that contain all the individual page in some `{}` and separate by `,`.

<br>

### _A. The Page Guideline_

Each page has the following two information :
  1. The `fileName` which defines the default __name of the file__ that will be saved for this page of the website.
 
  2. The `urlSelector` wich defines the string in the url that will differentiate this page from the others for the same website.

| variable | type | description |
|---|---|---|
| `fileName` | _string_ | the default __name of the file__ that will be saved for this page of the website website |
| `urlSelector` | _string_ | the __string__ in the url __that will differentiate this page__ from the others for the same website |

> 📖 For exemple, in the case of the page with the url :
> 
> `https://www.scrap-me.com/companies` , we can do :
> ```json
> "fileName": "ScrapMe_Companies",
> "urlSelector": "/companies",
> ```

<br>

### _B. The Page Rules_

The rules are defined in the `"rules"` array of rule.

You can add as many rules as you want to save information on the web page.

A rule allow you to define how you will select one data information that you want to save and under what form and what name you will save it.

💬 this is what the selenium will search for, here it's: class="companies"
💬 this is the name of the column in the csv
💬 this is the format of the saved information

<ins>example.json :</ins>
```json
"rules": [
    {
        "htmlTag": "class",
        "value": "companies",
        "saveAs": "Company Name",
        "saveType": "string"
    },
    {
        "htmlTag": "id",
        "value": "the-title-id",
        "saveAs": "Title",
        "saveType": "string"
    },
    {
        "htmlTag": "xpath",
        "value": "//section/dl/dd[2]",
        "saveAs": "Informations",
        "saveType": "string"
    },
    {
        "htmlTag": "xpath",
        "value": "//section/dl/dd[2]/a/span",
        "saveAs": "Website",
        "saveType": "link"
    }
]
```

```
    class, id, tag, name, link, partialLink, css, xpath
```

```
    string, link
```

<br>

### _The Page Basic Rule_

by using `"/"` as the selector to differentiate between all the link of a same website :
```"urlSelector": "/",```
you will create a set of pages that will work on any page of the website (because every `url` have the `/` charactère in it). This mean that __it's very important to put this rule at the bottom end of the list__ so it will be the last one to be applied if any other rule match.

------------------------------------------------------------

<br>

Error Message Box
=================

bla bla bla

------------------------------------------------------------

<br>

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

------------------------------------------------------------

## what have been done to launch project
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
