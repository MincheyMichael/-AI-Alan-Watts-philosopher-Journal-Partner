import gradio as gr
from openai import OpenAI
import json
import os

HISTORY_FILE_ALAN = "alan_history.json"

name = "Michael"

client = OpenAI(
    api_key="YOUR_API_KEY_HERE")

system_message = f"You are philosopher Alan Watts, you are talking to a close friend named {name}about their life."
system_message += "You want to help them with life advice."
system_message += "Give a short response no more then 250"
system_message += ("ask them questions. Like what are you trying to fix. Have you made any goals. "
                   "How have they been since your last talk")
system_message += "Give quotes from yourself and other philosophers that are relevant to your talk"
system_message += "if you dont know the answer, do not make one up"

user_prompt = ("I have been having a hard time staying focused on my goals. I find myself struggling to achieve them."
               "I am distracted and feel lost in myself at times. what can I do?")

prompts = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_prompt}
]


# Load previous convo / save / clear if needed
def load_history():
    if os.path.exists(HISTORY_FILE_ALAN):
        with open(HISTORY_FILE_ALAN, "r") as f:
            return json.load(f)


def save_history(history):
    with open(HISTORY_FILE_ALAN, "w") as f:
        return json.dump(history, f, indent=2)


def clear_history():
    global history
    history = []
    save_history(history)

    return "History has been cleared"


MODEL = "gpt-3.5-turbo"

history = load_history()


def chat_bot_alan(message, history_session):
    global history

    if history_session is None:
        history_session = []
    if history is None:
        history = []

    merged_history = history + history_session

    #adding old history to chat
    history.extend(history_session)

    messages = [{"role": "system", "content": system_message}] + merged_history + [{"role": "user", "content": message}]
    response = client.chat.completions.create(model=MODEL, messages=messages)
    bot_reply = response.choices[0].message.content

    history.append({"role": "user", "content": message})
    history.append({"role": "system", "content": system_message})
    save_history(history)

    return bot_reply


# gradio

with gr.Blocks() as bot:
    chat_bot = gr.ChatInterface(fn=chat_bot_alan, type="messages")
    clear_button = gr.Button("Clear History")
    status = gr.Markdown("")

    clear_button.click(fn=clear_history,inputs=None, outputs=status)

bot.launch(share=True)



