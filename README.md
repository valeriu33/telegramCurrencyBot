# telegramCurrencyBot

- Answers to command: /euro, /dollar, /all with prices for Euro and dollar in relation to MDL
- Every day at 08:00 UTC+3 sends euro and dollar prices
- Once in hour checks the price and sends a message when a currency price has changes with more than 0.2 MDL from yesterday


The application expects the following environment variables:
* [BOT_TOKEN](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
* [CHAT_ID](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/#get-your-telegram-chat-id) *For scheduled run, leave empty otherwise.*
* [API_KEY](https://free.currencyconverterapi.com/) *Get a free API-key. Don't forget to approve.*
