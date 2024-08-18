#    Copyright (c) 2021 Ayush
#    
#    This program is free software: you can redistribute it and/or modify  
#    it under the terms of the GNU General Public License as published by  
#    the Free Software Foundation, version 3.
# 
#    This program is distributed in the hope that it will be useful, but 
#    WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#    General Public License for more details.
# 
#    License can be found in < https://github.com/Ayush7445/telegram-auto_forwarder/blob/main/License >.

from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession

# Loglama yapılandırması
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

# Başlangıç mesajı
print("Bot başlatılıyor...")

# Ortam değişkenlerinden yapılandırmaları okuma
APP_ID = config("APP_ID", cast=int)
API_HASH = config("API_HASH", cast=str)
SESSION = config("SESSION", cast=str)
FROM_CHANNELS = config("FROM_CHANNEL", cast=lambda v: [int(i) for i in v.split(',')])
TO_CHANNELS = config("TO_CHANNEL", cast=lambda v: [int(i) for i in v.split(',')])

# Telegram istemcisini başlatma
try:
    client = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    client.start()
except Exception as e:
    logging.error(f"Telegram istemcisi başlatılırken hata oluştu: {e}")
    print(f"HATA - {e}")
    exit(1)

# Gelen yeni mesajları yakalayan event handler
@client.on(events.NewMessage(incoming=True, chats=FROM_CHANNELS))
async def forward_message(event):
    for to_channel in TO_CHANNELS:
        try:
            # Mesajı başka kanala iletme
            await client.send_message(to_channel, event.message)
            logging.info(f"Mesaj {event.chat_id} kanalından {to_channel} kanalına iletildi.")
            print(f"Mesaj {event.chat_id} kanalından {to_channel} kanalına iletildi.")
        except Exception as e:
            logging.error(f"Mesaj {to_channel} kanalına iletilirken hata oluştu: {e}")
            print(f"Mesaj {to_channel} kanalına iletilirken hata oluştu: {e}")

# Botu çalıştırma
print("Bot çalışmaya başladı. Mesajlar bekleniyor...")
client.run_until_disconnected()
