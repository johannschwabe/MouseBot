source venv/bin/activate
cd bot
nohup python3 bot.py>bot.log &
cd ../API
nohup uvicorn API:app --reload --host localhost>api.log &
 
