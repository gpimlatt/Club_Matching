# USC Club Matcher

## Description
USC Club Matcher attempts to match users to organized clubs based off a questionnaire provided by the user. A 
representative for each club will take an identical questionnaire. We find the 5 clubs with the closest similarity in 
terms of answers provided by the user.

The answer set for the user and each club are stored in separate vectors. The matching algorithm computes the [cosine
similarity](https://en.wikipedia.org/wiki/Cosine_similarity) between the users vector and the vector for each club.

## Install

#### Pipenv

This project uses `pipenv` as a package manager and virtual environment for Python. `Pipenv` is required to be installed prior 
to working on this project.  
[How to install `pipenv`](https://pipenv.pypa.io/en/latest/#install-pipenv-today)

#### NPM
This project uses `npm` as a package manager for javascript dev dependencies. `NPM` is helpful when working on static
files (`js` and `scss`).  
[How to install `npm`](https://www.npmjs.com/get-npm)

#### Clone `Club_Matching` from Github
```commandline
git clone git@github.com:WesternUSC/Club_Matching.git && cd Club_Matching/
```
#### Python dependencies from `Pipfile`
```commandline
pipenv install
```
#### Javascript dev dependencies from `package.json`
```commandline
npm install
```

## Setup

#### Start `gulpfile.js`
This project uses [Gulp](https://gulpjs.com/) as a build tool for automatically compiling Sass into CSS.  
```commandline
gulp
```

#### Start virtual environment
```commandline
pipenv shell
```

#### Launch Flask application (in debug mode)
```commandline
python run.py
```

The website should now be accessible on [localhost:5000](http://localhost:5000)

## Scripts

#### `import.py`
- Creating/updating club accounts from a JSON file.
- When executing this script you must provide a name of a JSON file which contains the club information. This file must 
be stored inside of `Club_Matcher/data/` prior to executing the command. Otherwise, a FileNotFound error will occur.
- How to execute this script: `python import.py filename.json`, where `filename.json` is 
`Club_Matcher/data/filename.json` and stores the club data.

#### `deletedb.py`
- Deletes all tables in the database. 
- How to execute this script: `python deletedb.py`

#### `createdb.py`
- Creates all tables in the database as specified in `Club_Matcher/clubmatcher/main/models.py`
- How to execute this script: `python createdb.py`

#### `resetdb.py`
- Combines `deletedb.py` and `createdb.py` into one step to effectively reset the database.
- How to execute this script: `python resetdb.py`

#### `run.py`
- Runs the Flask application in debug mode.
- How to execute this script: `python run.py`

## JSON Club Data Format
Unless `import.py` is changed to support another format, your JSON club data file should be in the following format:
```json
[ // File located in `Club_Matcher/data/`
  {
    "ProductID": 1,
    "SKU": 1,
    "Name": "",
    "Email": "...@westernusc.ca",
    "Storefront Link": "https://westernusc.store/...",
    "WL Address": "https://www.westernlink.ca/organization/...",
    "Tags": "",
    "Short description": ""
  },
  {
    "ProductID": 2,
    "SKU": 2,
    "Name": "",
    "Email": "...@westernusc.ca",
    "Storefront Link": "https://westernusc.store/...",
    "WL Address": "https://www.westernlink.ca/organization/...",
    "Tags": "",
    "Short description": ""
  },
  // ...
]
```
**Note**: Each club uses the `SKU` as its primary key when stored in the database. Therefore, all SKU's should be
unique, otherwise the existing club's information will the same `SKU` will be overwritten during import.
