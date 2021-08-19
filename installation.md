
Requirements:

  1. You should have python3 installed
  2. Ubuntu based system


Installation Instructions:

  1. Create a new folder

  2. Unzip files into folder

  3. Your directory should look like this:
      -  /FlaskApp
      -  /requirements.txt
      -  /dummydata.py
      -  /installation.md

  4. Open your terminal in the folder and run the following commands:
    - python3 -m venv projenv
    - source projenv/bin/activate
    - export FLASK_APP="FlaskApp"
    - pip install -r requirements.txt
    - flask run

  5. To restart the server run the following commands:
    - fuser -k 5000/tcp
    - flask run
