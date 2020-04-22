# telegramCurrencyBot

- Answers to command: /euro, /dollar, /all with prices for Euro and dollar in relation to MDL
- Every day at 08:00 UTC+3 sends euro and dollar prices
- Once in hour checks the price and sends a message when a currency price has changes with more than 0.2 MDL from yesterday


after ```git clone``` add new file in the project folder, name it ```secrets.py``` and add three lines of code:
```
BOT_TOKEN = 'your telegram bot'
CHAT_ID = your chat id
API_KEY = 'your API key'
```

BOT_TOKEN: you can get from here: https://core.telegram.org/bots#3-how-do-i-create-a-bot

CHAT_ID: here's how to get it: https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/#get-your-telegram-chat-id

API_KEY: login here and take your free API-key: https://free.currencyconverterapi.com/
