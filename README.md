# agy-rest-server

Just a tool help me stuff

In my current job, My daily works require me make a bunch of judgement. which is tired as hell.

So i wish to make a agent which take restapi http get and with skills setup and easily solve my works.

## Setup

```bash
bash setup.sh
```

This create the .venv folder and take requirements.txt

## Run

```bash
bash run.sh API_KEY1
# or 
bash run.sh API_KEY1,API_KEY2
```

In python code it use split function to seperate the api
This mean it can take multiple free tier api key for maximized the free tier usage
