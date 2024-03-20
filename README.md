# Py-UNO

## Description

This project is a clone of the popular card game UNO, developed using Pygame as part of our senior capstone project. It currently supports single-player mode against AI opponents, with plans to introduce a multiplayer feature in the near future.

## Installation

To run Py-Uno, you'll need Python installed on your system. This game has been tested with Python 3.8, but it should be compatible with newer versions as well. Follow the steps below to set up your environment and start playing:

1. **Clone the Repository**

    First, clone this repository to your local machine using Git:

    ```bash
    git clone https://github.com/mgarza86/Uno.git
    cd uno-clone
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

To start the game, navigate to the project's root directory and run the `scene_manager.py` script:

```bash
python scene_manager.py
```
For macOS and Linux users, you might need to use python3 instead of python:

```bash
python3 scene_manager.py
```

