# Task Management System

## How to setup the environment

* Install [pyenv](https://github.com/pyenv/pyenv#installation)

* Install Python 3.13

```bash
pyenv install 3.13
```

* Setup and activate the virtual environment

```bash
pyenv virtualenv 3.13 tms
pyenv local tms
```

* Install the required packages
```bash
pyenv exec pip install -r requirements.txt 
```

## Continuous Integration

To check whether the codebase follows the best practices, run the linter

```bash
ruff check
```
