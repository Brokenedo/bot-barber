from telegram import *
from telegram.ext import *
from requests import *


class Prestazione:
    def __init__(self, cliente):
        self.cliente = cliente
        self.tipo = ""
        self.costo = 0
        self.ora = ""
        self.giorno = "2"

updater = Updater(token="1777961472:AAH8Z7I1949Sy5mXENAKoBMHjmj17uFN2uo")
dispatcher = updater.dispatcher

taglio = "Taglio"
barba = "Barba"
taglioBarba = "TaglioBarba"

randomPeopleUrl = "https://thispersondoesnotexist.com/image"
randomPImageUrl = "https://picsum.photos/1200"

likes = 0
dislikes = 0
allowedUsernames = ["Broken202108"]


def startCommand(update: Update, context: CallbackContext):
    global prestazioneCliente
    prestazioneCliente = Prestazione(update.effective_chat.username)
    buttons = [[KeyboardButton(taglio)], [KeyboardButton(taglioBarba)], [KeyboardButton(barba)]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Ciao {prestazioneCliente.cliente} scegli cosa vuoi fare",
                             reply_markup=ReplyKeyboardMarkup(buttons))


def messageHandler(update: Update, context: CallbackContext):
    if update.effective_chat.username not in allowedUsernames:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot")
        return
    if taglio in update.message.text:
        prestazioneCliente.tipo = taglio
    if barba in update.message.text:
        prestazioneCliente.tipo = barba
    if taglioBarba in update.message.text:
        prestazioneCliente.tipo = taglioBarba

    if prestazioneCliente:
        buttons = [[InlineKeyboardButton("Si", callback_data="YES")], [InlineKeyboardButton("No", callback_data="NO")]]
        message = f"Hai scelto {prestazioneCliente.tipo} il costo è di {prestazioneCliente.costo} Euro.\nVuoi continuare?"
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
                                 text=message)


def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

    global likes, dislikes

    if "YES" in query:
        likes += 1
        prestazioneCliente.ora = "22:00"
        print(prestazioneCliente.ora)

    if "NO" in query:
        dislikes += 1

    print(f"likes => {likes} and dislikes => {dislikes}")


def main():
    dispatcher.add_handler(CommandHandler("start", startCommand))
    dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
    dispatcher.add_handler(CallbackQueryHandler(queryHandler))

    updater.start_polling()


if __name__ == '__main__':
    main()
