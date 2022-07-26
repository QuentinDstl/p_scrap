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
     - a. the page guideline
     - b. the page rules
     - c. the page basic rule (_optional_)

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

### ___a. the page guideline___

Each page has the following two information :

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

### ___b. the page rules___

The rules are defined in the `"rules"` array of rule.

A rule allow you to define how you will select one data information that you want to save and under what form and what name you will save it.

> 📖 You can add as many rules as you want to save information on the web page.

A rule have the following information :

| variable | type | description |
|---|---|---|
| `htmlTag` | _string_ | a [html tag](#html-tags) that the selenium will search for |
| `value` | _string_ | the value of the data that the html tag have |
| `saveAs` | _string_ | the name of the column for this information in the csv |
| `saveType` | _string_ | the [saving type](#saving-types) that will define format of the data |


> 📖 For exemple, in the case of the following html tag :
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

    > ⚠️ Only the __first corresponding tag__ will be save !
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

    > [🚩 Get more Informations on Xpath](https://www.geeksforgeeks.org/introduction-to-xpath/) or [Use Xpath Extension](https://chrome.google.com/webstore/detail/xpath-finder/ihnknokegkbpmofmafnkoadfjkhlogph?hl=en)


#### saving types:

- string
    > to save any type of data
- link
    > to save link data from href tag


<br>

### ___c. the page basic rule___

by using `"/"` or `""` as the `urlSelector` you will create a __page basic rule__. 

This mean that the following scrapping rule will apply on every page of the website. This will happen because every `url` have the `/` character in it. 

> ⚠️ This rule have to be __at the bottom end of the list of pages__ so it will be the last one to be applied if any other page match the previous url selector.

You can use this selector so if some website dont use any specific string in the url for the page you want to scrap (if they use _random token_ or _user id string_), you can use it.

------------------------------------------------------------

<br>

Error Messages
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
