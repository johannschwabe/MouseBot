cd /home/pi/MouseBot/
source venv/bin/activate
cd bot
nohup python3 bot.py>bot.log &
cd ../API
nohup uvicorn API:app --reload --host 192.168.4.1>MouseBotapi.log &
 
