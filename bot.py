from telethon import TelegramClient, events
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import re
import time
import requests
import random

Token = "7449000581:AAF07hXqSjg2tUpFpUtYbsernZeTUg_S_ec"
id_channel = -1002491497720  # ID de tu canal objetivo

api_id = 29337352
api_hash = 'da5a8256269380850cd718c6e6475fb9'

client = TelegramClient('cheemschk', api_id, api_hash)
client.parse_mode = 'html'

bot = TeleBot(Token, parse_mode="html")

def verificar(ccn):
    # Verificar la tarjeta en tu base de datos
    with open('tarjetas.txt', 'r') as f:
        tarjetas = f.readlines()
    
    for tarjeta in tarjetas:
        tarjeta = tarjeta.strip()  # Eliminar espacios en blanco y caracteres especiales
        if ccn == tarjeta:
            return True
    
    return False

def obtener_tipo_gateway(texto):
    match_gateway = re.search(r'Gateway ➣[^\w]*(\w+)', texto)
    if match_gateway:
        return match_gateway.group(1)
    
    return None

@client.on(events.NewMessage)
async def my_event_handler(event):
    text = event.raw_text

    if "|" in text:
        x = re.findall(r'\d+', text)
        if len(x) < 4:
            print(f'! Tarjeta no detectada\n')
            return
        cc = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]
        if len(cc) > 16:
            return
        if len(mm) > 11:
            return
        if len(yy) > 4:
            return
        if len(cvv) > 4:
            return
        cxc = f"{cc}"
        if mm.startswith('2'):
            mm, yy = yy, mm
        if len(mm) >= 3:
            mm, yy, cvv = yy, cvv, mm
        if len(cc) < 15 or len(cc) > 16:
            print(f'! Tarjeta invalida\n')
            return
        if len(yy) == 2:
            yy = '20' + yy

        tarj = f'{cc}|{mm}|{yy}|{cvv}'
        v = verificar(cc)
        if v == True:
            print(f'{tarj} Esta tarjeta ya existe en la base de datos')
            return
        tarj = f'{cc}|{mm}|{yy}|{cvv}'
        with open('tarjetas.txt', 'a') as d:
            d.write(tarj + "\n")

        # res = gate(cc, mm, yy, cvv)
        if 'Approved' == 'Approved':
            mes = '✅ Approved - ' + tarj + ''
            photo_path = "Jsjs.jpg"  # Ruta de la imagen que deseas enviar

            bin = cxc[0:6]
            rs = requests.get(f"https://bins.antipublic.cc/bins/{bin}").json()
            country = rs["country_name"]
            flag = rs["country_flag"]
            bank = rs["bank"]
            brand = rs["brand"]
            type = rs["type"]
            level = rs["level"]

            lines = text.split("\n")  #split message
            gateway = ""  # store gateway
            for line in lines:  # check every lines
                if "Gateway" in line:
                    gateway = obtener_tipo_gateway(line)
                    if gateway:
                        gateway = f"Gateway ➵ {gateway}"
                    break

            status = "APROVEDD"  # Definir el valor de la variable status

            text = f"""
❖ <b>SCRAPPER CHEEMSCHK</b>❖

#Bin{bin}

<b>↓→𝙀𝙭𝙩𝙧𝙖: </b> <code>{cxc[0:12]}xxxx|{mm}|{yy}|xxx</code> 
━━
<b>↓→𝘾𝙖𝙧𝙙: </b> <code>{cc}|{mm}|{yy}|{cvv}</code>
<b>↓→𝙎𝙩𝙖𝙩𝙪𝙨: ↳ </b> {status} ❇️
↓→𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚: ↳ <code>APROVEDD</code>
━━━━━━━━━━━━
<b>↓→𝙄𝙣𝙛𝙤: </b> <code>{brand}</code> - <code>{level}</code> - <code>{type}</code>
<b>↓→𝘽𝙖𝙣𝙠: </b> <code>{bank}</code>
<b>↓→𝘾𝙤𝙪𝙣𝙩𝙧𝙮: </b> <code>{country} - [{flag}]</code>
❖❖❖❖❖❖❖❖❖❖❖❖❖❖❖❖❖❖❖❖❖❖❖❖❖
        ━━━━━ [Scrapper CHEEMSCHK] ━━━━━
            """

            print(f'$ Mensaje enviado -> {cc}|{mm}|{yy}|{cvv}\n')
            time.sleep(0.5)
            
            # Crear el teclado en línea
            keyboard = InlineKeyboardMarkup()
            button_owner = InlineKeyboardButton("OWNER", url="https://t.me/chkcheems")
            button_semiowner = InlineKeyboardButton("SEMI OWNER", url="t.me/chkcheems")
            button_chat = InlineKeyboardButton("CHAT VIP", url="https://t.me/chkcheems")
            keyboard.add(button_owner, button_semiowner, button_chat)

            with open('Jsjs.jpg', 'rb') as photo:
                bot.send_photo(id_channel, photo, caption=text, reply_markup=keyboard)
        else:
            pass

card_regex = re.compile(r'\b(?:\d[ -]*?){13,19}\b')  # Expresión regular para números de tarjeta
date_regex = re.compile(r'\b(\d{2})[/.,-](\d{2})[/.,-](\d{2}|\d{4})\b')  # Expresión regular para fechas de vencimiento
cvv_regex = re.compile(r'\b\d{3,4}\b')  # Expresión regular para CVV

def custom_function(card_number, expiration_month, expiration_year, cvv):
    # Validar la tarjeta de crédito
    if validate_credit_card(card_number):
        print(f'Tarjeta detectada -> {card_number}|{expiration_month}|{expiration_year}|{cvv}')
    else:
        print('Tarjeta inválida')

def validate_credit_card(card_number):
    # Realizar la validación de la tarjeta de crédito (puedes implementar tu lógica de validación aquí)
    # Por ejemplo, puedes utilizar bibliotecas como "pycard" o "pycreditcard"
    # Devuelve True si la tarjeta es válida, False en caso contrario.
    return True

@client.on(events.NewMessage)
async def my_event_handler(event):
    text = event.raw_text

    if "|" in text:
        x = re.findall(r'\d+', text)
        if len(x) < 4:
            print(f'Tarjeta no detectada\n')
            return
        cc = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]


print("PROGRAMA INICIADO TLG\nVERSION: 2.0\n")

client.start()
client.run_until_disconnected()