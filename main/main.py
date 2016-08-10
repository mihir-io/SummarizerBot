import logging
import validators

from newspaper import Article
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from analysis import Summarizer

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define command handlers.
def bot_start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi, thanks for using SummarizerBot!\n\n'
                                                 'Please provide me with a link to your news article and I will '
                                                 'do my best to summarize it for you!')


def bot_help(bot, update):
    bot.sendMessage(update.message.chat_id, text="/help -- this help message\n"
                                                 "/summarize [URL] -- returns a summary of the article provided")


def bot_error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def summarize(bot, update):
    user_message = str(update.message.text)
    if(user_message.startswith('/summarize')):
        user_message = user_message.split(' ',1)[1]
    logger.info(user_message)
    if not validators.url(user_message):
        bot.sendMessage(update.message.chat_id,
                        text="Unfortunately, I can't summarize something that is not a URL. Send me an article URL and I'll try to summarize it!")
    else:
        article = Article(user_message)
        article.download()
        article.parse()

        # if not article.is_valid_url(): bot.sendMessage(update.message.chat_id, text="Couldn't parse article!")

        bot.sendMessage(update.message.chat_id, text=Summarizer.summarize_text(article.text))

def main():
    # Create the EventHandler and pass it your bot's token.

    updater = Updater("***REMOVED***")

    # Get the dispatcher to register handlers

    dp = updater.dispatcher

    # on different commands - answer in Telegram

    dp.add_handler(CommandHandler("start", bot_start))

    dp.add_handler(CommandHandler("help", bot_help))

    dp.add_handler(CommandHandler("summarize", summarize))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], summarize))

    # log all errors
    dp.add_error_handler(bot_error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
