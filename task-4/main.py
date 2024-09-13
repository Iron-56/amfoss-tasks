import telebot
from telegram.constants import ParseMode
from google_books_api_wrapper.api import GoogleBooksAPI


bot = telebot.TeleBot("7286486071:AAELBZ1SfvlSRPA92pVcLdf6b-LU0w60soA")
client = GoogleBooksAPI()

welcome_message = """------------- MENU ----------------
A Bot for assisting in book recommendation.
type /help: for more command list
"""

command_list = """--------------- COMMANDS ---------------
	/start:   Welcome page.
	/book:    select genre.
	/preview: select book name.
	/list:    To display reading list.
	/help:    For command.
"""

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, welcome_message)


@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, command_list)

def create_html_table(data):
	html  = "<table>\n"
	html += "	<thead>\n"
	html += "		<tr>\n"
	html += "			<th>TITLE</th>\n"
	html += "			<th>AUTHOR</th>\n"
	html += "		</tr>\n"
	html += "	</thead>\n"
	html += "	<tbody>\n"

	for row in data:
		html += "		<tr>\n"
		html += f"			<td>{row[0]}</td>\n"
		html += f"			<td>{row[1]}</td>\n"
		html += "		</tr>\n"

	html += "	</tbody>\n"
	html += "</table>"

	return html

def genre(message):
	subject = client.get_books_by_subject(message.text) 
	books = subject.get_all_results()[:10]
	data = []

	for book in books:
		data.append([book.title, book.authors[0]])
	
	table = create_html_table(data)
	print(table)
	bot.send_message(chat_id=message.chat.id, text=table, parse_mode=ParseMode.HTML)

@bot.message_handler(commands=['book'])
def book(message):
	msg = bot.send_message(message.chat.id, "Enter a genre: ")
	bot.register_next_step_handler(msg, genre)

bot.infinity_polling()
