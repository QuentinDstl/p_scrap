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
| `[SAVING] SAVE_DATA_PATH` | _C:/Folder/To/Save/the_result.csv_ | folder where the current website will be saved |

> ⚠️ If `.config` doesn't exist, it will be created on next launch and you will be asked to choose it.


.env file
---------

| what is in `.env` |||
|---|---|---|
| `DIR_CHROMEAPP_PATH` | _C:/Program Files/Google/Chrome/Application/_ | default folder used to launch Chrome on debugging mode |
| `PORT` | _9222_ | default port used to launch the new chrome window |

> ⚠️ The `PORT` must __not be used by another app__. Launch `cmd` with admin rights and execute : `netstat -a` to see what port are used.

> 📖 To get the `DIR_CHROMEAPP_PATH` :
> ```
> 1. Window + S: to start a research
> 2. Now search for `Chrome`
> 3. Righ-click on the logo that just pops
> 4. Click on: Open File Location
> 5. In the new window, right-click on `Google Chrome` shortcut file
> 6. Click on: Open File Location
> 7. Copy, paste the path of the newly opened folder into the `.env` file
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
 
 A template has 2 important parts:
  1. The Template Specific Name
  2. The Template List of Pages
     - a. The page guideline
     - b. The page rules
     - c. The page basic rule (_optional_)

<br>

### ___1. Template Specific Name___

The __name__ of the template file : `name.json` is important as it will be the string used to load it.

> 📖 For example, if you want to scrap data on the website `https://www.scrap-me.com`, you will need to create a `scrap-me.json` template file.

<br>

### ___2. The Template List of pages___

A website can have many different pages. For example `https://www.scrap-me.com` can have the following pages :
- `https://www.scrap-me.com/profiles`
- `https://www.scrap-me.com/companies`

We can create different scrapping rules for each one of them or create a basic rule that will apply to every page.

You will find in the template a `"pages"` array that contains all the individual page in some `{}` and separate by `,`.

<br>

### ___a. The page guideline___

Each page has the following two information :

| variable | type | description |
|---|---|---|
| `fileName` | _string_ | the default __name of the file__ that will be saved for this page of the website website |
| `urlSelector` | _string_ | the __string__ in the url __that will differentiate this page__ from the others for the same website |

> 📖 For example, in the case of the page with the url :
> 
> `https://www.scrap-me.com/companies` , we can do :
> ```json
> "fileName": "ScrapMe_Companies",
> "urlSelector": "/companies",
> ```

<br>

### ___b. The page rules___

The rules are defined in the `"rules"` array of rule.

A rule allows you to define how you will select one data information that you want to save and under what form and what name you will save it.

> 📖 You can add as many rules as you want to save information on the web page.

A rule has the following information :

| variable | type | description |
|---|---|---|
| `htmlTag` | _string_ | a [html tag](#html-tags) that the selenium will search for |
| `value` | _string_ | the value of the data that the html tag has |
| `saveAs` | _string_ | the name of the column for this information in the CSV |
| `saveType` | _string_ | the [saving type](#saving-types) that will define the data format |


> 📖 For example, in the case of the following html tag :
> ```html
> <p class="company-title"> Super Company Name </p>
> ```
> We can create the following rule :
> ```json
>    {
>        "htmlTag": "class",
>        "value": "company-title",
>        "saveAs": "Company Name",
>        "saveType": "string"
>    }
> ```

> 📖 In the case of the following html tag with a link :
> ```html
> <a href="https://www.scrap-me.com/"> Our Website </a>
> ```
> We can create the following rule :
> ```json
>    {
>        "htmlTag": "link",
>        "value": "Our Website",
>        "saveAs": "Company Link",
>        "saveType": "link"
>    }
> ```

#### html tags:

- class :
    > ```html
    > <div class="text container company">...</div>
    > ```
    > the rule `value` could here be `company` or `text`

    > ⚠️ Only __one__ class can be passed !
- id
    > ```html
    > <div id="company-name"> Company Name </div>
    > ```
    > the rule `value` will here be `company-name`
- tag
    > ```html
    > <h1> Company Name </h1>
    > ```
    > the rule `value` will here be `h1`

    > ⚠️ Only the __first corresponding tag__ will be saved !
- name
    > ```html
    > <input name="username" type="text" />
    > ```
    > the rule `value` will here be `username`
- link
    > ```html
    > <a href="https://scrap-me.com/"> A Link </a>
    > ```
    > the rule `value` will here be `A Link`
- partialLink
    > ```html
    > <a href="https://scrap-me.com/"> A Link </a>
    > ```
    > the rule `value` could here be `link` or `A Li`
- css
    > 📖 a very flexible html tag selector :
    > ```html
    > <p> Welcome on </p><p> Scrap-Me </p><p> ! </p>
    > ```
    > the rule `value` will here be `p.content:nth-child(2)` to select the _Scrap-Me_
- xpath
    > 📖 the most flexible html tag selector :
    > ```html
    > <div class="informations">
    >     <img src="https://img.png" alt="logo" />
    >     <p> Company Name </p>
    > </div>
    > ```
    > the rule `value` will here be `//div[@class='name']/p`

    > [🚩 Get more Information on Xpath](https://www.geeksforgeeks.org/introduction-to-xpath/) or [Use Xpath Extension](https://chrome.google.com/webstore/detail/xpath-finder/ihnknokegkbpmofmafnkoadfjkhlogph?hl=en)


#### saving types:

- string
    > to save any type of data
- link
    > to save link data from href tag


<br>

### ___c. The page basic rule___

By using `"/"` or `""` as the `urlSelector` you will create a __page basic rule__. 

This means that the following scrapping rule will apply to every page of the website. This will happen because every `url` has the `/` character in it. 

> ⚠️ This rule has to be __at the bottom end of the list of pages__ so it will be the last one to be applied if any other page matches the previous url selector.

You can use this selector so if some website doesn't use any specific string in the url for the page you want to scrap (if they use _random token_ or _user id string_), you can use it.

------------------------------------------------------------

<br>

Error Messages
=================

Critical Errors
---------------

> 📖 Critical errors will appear in a popup error window.

| Id | Description | Solution |
|---|---|---|
| `#10` | Can't execute the terminal commands to set chrome.exe path or to open a chrome debugging instance | Try to launch it manually in your terminal by running [this command](#openning-chrome-debugging-instance) and see if it work |
| `#11` | The selenium driver don't work | Download the [latest version of chromedriver](https://chromedriver.storage.googleapis.com/index.html) and replace the previous `chromedriver.exe` in the `driver` folder |

Warnings
--------

> 📖 Warnings will appear in the application console.

| Id | Description | Solution |
|---|---|---|
| `#20` | One of the [rules](#b-the-page-rules) is not working properly | Check the missing information in the `.csv` saved file and change the field `value` or `htmlTag` corresponding in the same template file |
| `#21` | Name has special characters in it | The name given to the csv file have special characters please only use letters, numbers and `-` or `_` |
| `#22` | Loading templates error | The templates is not founded  |
| `#23` | Loading templates error | The templates is not founded  |
| `#24` | The `htmlTag` in one of the rule of the template is not one of the [html tag](#html-tags) | Open the template file of the website you where trying to save and search for the corresponding tag-name that was prompt in console |


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
│   └── ...     # templates for scraping data from a website
├── .config     # file with user configuration 
├── .env        # file with general configuration
├── .gitignore  # file with all the ignored files in git
├── scrap.exe   # file with the compiled main program
├── scrap.py    # file with the main program
├── README.md   # file with general information
└── requirements.txt # file with all the dependencies
```
Openning Chrome Debugging Instance
----------------------------------

We are using python `Popen` to execute a child program in a new process. We then wait for the execution and then kill the subprocess.

The child program will :
  1. Set the chrome driver path
  2. Open a new chrome window with a the debugging mode

You can manually execute the child program by running the following command in your terminal after changing the `DIR_CHROMEAPP_PATH` and the `PORT` values :

```bash
set PATH=%PATH%;DIR_CHROMEAPP_PATH&&chrome.exe --remote-debugging-port=PORT --user-data-dir="C:\TestFolder\ChromeScraperProfile"
```

> 📖 look here to see what [path and port values](#env-file) you need to set to make it work for you

------------------------------------------------------------

## what have been done to launch the project
pip install all the requirements in requirements.txt

https://nuitka.net/doc/user-manual.html

## TODO V2
SPEED :
use pypy3
use numpy for matrix and use jit on top of it

http://sdz.tdct.org/sdz/creer-une-installation.html


refacto :
        rule -> page
        saveAs -> rule

no .env
no assets