# Task Management System

![Ruff](https://github.com/SeoulSKY/TaskManagementSystem/actions/workflows/ruff.yml/badge.svg)
![Pytest](https://github.com/SeoulSKY/TaskManagementSystem/actions/workflows/pytest.yml/badge.svg)
[![codecov](https://codecov.io/gh/SeoulSKY/TaskManagementSystem/graph/badge.svg?token=TA1IBHAWSS)](https://codecov.io/gh/SeoulSKY/TaskManagementSystem)

## How to setup the environment

### Option 1

* Install [Docker](https://www.docker.com/get-started/)

#### How to Run

Run the following command

```bash
docker compose up --build
```

Click [here](http://localhost:8000) to use the task management system with a web browser.

### Option 2

* Install [pyenv](https://github.com/pyenv/pyenv#installation)

* Install Python 3.13

```bash
pyenv install 3.13
```

Setup and activate the virtual environment

```bash
pyenv virtualenv 3.13 tms
pyenv local tms
```

Install the required packages

```bash
pyenv exec pip install -r requirements.txt 
```

#### How to Run

Run the following command.

```bash
pyenv exec fastapi dev main.py
```

Click [here](http://localhost:8000) to use the task management system with a web browser.

## Continuous Integration

### Pipelines

This repository uses GitHub Actions for implementing CI pipelines.

![Ruff](https://github.com/SeoulSKY/TaskManagementSystem/actions/workflows/ruff.yml/badge.svg) — Result of linting for coding style.

![Pytest](https://github.com/SeoulSKY/TaskManagementSystem/actions/workflows/pytest.yml/badge.svg) — Result of running test suites.

[![codecov](https://codecov.io/gh/SeoulSKY/TaskManagementSystem/graph/badge.svg?token=TA1IBHAWSS)](https://codecov.io/gh/SeoulSKY/TaskManagementSystem) — Result of the code coverage testing.

### Manual

To check whether the codebase follows the best practices, run the linter

```bash
pyenv exec ruff check
```

To run the test suite, run the following command

```bash
pyenv exec pytest tests --cov
```
