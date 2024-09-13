### My Approach

I used telebot as a port to telgram app that can be used to interact with the user.

```python
@bot.message_handler
```

This decorator lets us to register a function when the user sends a specific command.

```python
register_next_step_handler
```
This function lets us to register a function when the user sends a word instead.

```python
send_message
```
This function sends message to user

```python
subject = client.get_books_by_subject(message.text) 
books = subject.get_all_results()
```

This block gets the list of books of a subject