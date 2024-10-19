import telebot
from booking import flight, BookingError

TOKEN = '*** ВСТАВЬТЕ ТОКЕН ВАШЕГО БОТА ***'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Здравствуй, я могу забронировать для тебя места в самолёте.")
    bot.send_message(message.chat.id, "```\n" + flight.get_configuration() + "\n```", parse_mode="MarkdownV2")
    bot.send_message(message.chat.id, "*Что бы забронировать место*:\n"
                                      "выбери свободное и отправь мне в виде числа и буквы \(номер ряда и кресло\), "
                                      "например:\n"
                                      "```\n12A\n```", parse_mode="MarkdownV2")


@bot.message_handler(content_types=['text'])
def repeat_user_message(message):
    try:
        id_seat = message.text.strip().lower()
        flight.book_seat(int(id_seat[:-1]), id_seat[-1])
        bot.send_message(message.chat.id, f"Место `{id_seat.upper()}` успешно забронировано", parse_mode="MarkdownV2")
        bot.send_message(message.chat.id, "```\n" + flight.get_configuration() + "\n```", parse_mode="MarkdownV2")
    except BookingError as err:
        bot.send_message(message.chat.id, str(err))
    except Exception:
        bot.send_message(message.chat.id, "Неверный ввод")


print('Сервер запущен.')
bot.polling(
    non_stop=True,
    interval=1
)
