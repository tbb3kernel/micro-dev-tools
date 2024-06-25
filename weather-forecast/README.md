# Weather Forecast Application with Open-meteo API!

## Setup python

You need `python3` of course or any tool of your choice to send HTTP request
to open-meteo API endpoint.

for my choice I use `python3` with `requests` library to make my life easier!

### Setup virtual environment

```bash
export ENV_NAME=<some-name>
python3 -m venv $ENV_NAME
source ./$ENV_NAME/bin/activate
pip install -r requirements.txt
```

## Run the application

Simply enter
`python3 forecast.py` also you can config the option in command line argument.
See the full list in `python3 forecast.py --help`
