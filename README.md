# To install

Install python 3 at a minimum

`
brew install python3
`

Create python virtual environment to run in this is named "venv"

`
python3 -m venv venv
`

Now you must activate the virtual environment! <br>
Very important to run in virtual environment if executing from cmd line

`
source venv/bin/activate
`

Install dependencies

`
pip install -r requirements.txt
`

# To Run
Two run options depending on flavor of the week

## Option 1
1. Add file to html dir in project
2. execute app.py python file will read and insert data into csv

## Option 2
execute app.py with arg of "path to html file
"