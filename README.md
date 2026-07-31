# agy-rest-server

Just a tool help me stuff

In my current job, My daily works require me make a bunch of judgement. which is tired as hell.

So i wish to HTTP server which will use ai agent which have skills setup can easily solve my daily works.

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

In python code it use split function to seperate the api keys\
This means it can take multiple api keys for maximized the free tier usage
