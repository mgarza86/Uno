# Py-UNO

## Description

This project is a clone of the popular card game UNO, developed using Pygame as part of our senior capstone project. It currently supports single-player mode against AI opponents, and limited multiplayer.

## Installation

To run Py-Uno, you'll need Python installed on your system. This game has been tested with Python 3.8, but it should be compatible with newer versions as well. Follow the steps below to set up your environment and start playing:

1. **Clone the Repository**

    First, clone this repository to your local machine using Git:

    ```bash
    git clone https://github.com/mgarza86/Uno.git
    cd uno
    ```

2. **Create and Activate a Virtual Environment (Optional but Recommended)**

    It's a good practice to create a virtual environment for Python projects to manage dependencies more effectively. You can do this by running:

    - For Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

    - For macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. **Install Dependencies**

    With your virtual environment activated, install the project dependencies by running:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Game

To start the game, navigate to the project's root directory and run the `main.py` script:

```bash
python main.py
```
For macOS and Linux users, you might need to use python3 instead of python:

```bash
python3 main.py
```

## Running Unit Tests

To ensure the functionality of the game components, you can run the unit tests provided in the project. From the root directory of the project, execute the following command to run all tests:

```bash
python -m unittest discover -s tests -v
```
This command will discover and run all tests within the tests directory, giving you a verbose output of the test results.

## Running the Server

From the root directory, run:

```bash
python server.py
```
While the server runs in one terminal, you can launch the app and connect through the multiplayer page.