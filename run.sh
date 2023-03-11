# run API on local at port 8789
# command : $source run.sh on termminal
source ./venv/bin/activate # use virtual environment
uvicorn main:app --port 8789