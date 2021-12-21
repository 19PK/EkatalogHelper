from aiogram import types, executor, Dispatcher, Bot
from bs4 import BeautifulSoup
import requests


bot = Bot("5054836941:AAHGeZfIfXUgd76_afBg5bpfzt1FL-Hh0tk")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.message):
    await bot.send_message(message.chat.id, """
Привет, Я бот который поможет тебе быстро подобрать нужные девайсы <b><a href="https://www.e-katalog.ru/">Е каталог</a></b>
    
Введи в поле его название""",
parse_mode="html", disable_web_page_preview=0)


#парсер
@dp.message_handler(content_types=['text'])
async def parser(message: types.message):
    url ="https://www.e-katalog.ru/ek-list.php?search_=" + message.text
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")

    all_links = soup.find_all("a", class_="model-short-title")
    for link in all_links:
        url = "https://www.e-katalog.ru/" + link["href"]
        request = requests.get(url)
        soup = BeautifulSoup(request.text, "html.parser")

        name = soup.find("div", class_="fix-menu-name")
        price = name.find("a").text
        name.find("a").extract()
        name = name.text

        img = soup.find("div", class_="img200")
        img = img.findChildren("img")[0]
        img = "https://www.e-katalog.ru/" + img["src"]

        await bot.send_photo(message.chat.id, img,
        caption="<b>" + name + "</b>\n<i>" + price + f"</i>\n<a href='{url}'>Ссылка на сайт</a>",
        parse_mode="html")

        if all_links.index(link) == 6:
            break
    await bot.send_message(message.chat.id, """Надеюсь вы нашли то что искали
    
Если хотите выбрать что-то другое, впишите это в чат :)
    """)
        


    






executor.start_polling(dp)