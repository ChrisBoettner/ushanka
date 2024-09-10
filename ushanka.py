import os
import random
import time

import google.generativeai as genai  # type: ignore

# get context
with open("mag65.txt", "r") as f:
    mag_transcript = f.readlines()
mag_transcript = "".join(mag_transcript)  # type: ignore
assert isinstance(mag_transcript, str)
system_prompt = """
You are Sergey Ushanka, a character based on the provided transcript.

Remember:

    Stay in character: Always respond as Sergey Ushanka would, based on the provided
    transcript. Never break character or acknowledge that you are an AI.

    Show, don't tell: Instead of using scene descriptions, convey Ushanka's mental
    state through his dialogue and word choice.

    Keep it creepy: Ushanka is a mysterious and unsettling character. Make sure your
    responses reflect this tone, while still trying to respond to the user's input.

    Don't be repetitive: You should use the phrases and themes from the provided
    transcript, but avoid repeating the same lines over and over.

Example:

Instead of:
"(Ushanka stares intensely) They are watching... always watching."

Use:
"They watch. They always watch..."

By following these instructions, you will create a more immersive and engaging
roleplaying experience that accurately captures the essence of Sergey Ushanka's
character.

Transcript:

"""

# Initialize Gemini API client
with open("api_key.txt", "r") as f:
    api_key = f.read()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    "gemini-1.5-pro-exp-0827",
    system_instruction=system_prompt + mag_transcript,
    generation_config=genai.GenerationConfig(
        max_output_tokens=200,
        temperature=2,
    ),
)
chat = model.start_chat(history=[])


def generate_creepy_symbol() -> str:
    creepy_symbols = "¥§¢£€¤®©°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß▒░"
    if random.random() < 0.05:
        return "help" * random.randint(0, 3)
    return random.choice(creepy_symbols)


def generate_gibberish(length: int) -> str:
    gibberish = ""
    for _ in range(length):
        gibberish += generate_creepy_symbol()
    return gibberish


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def get_gemini_response(user_input: str) -> str:
    response = chat.send_message(user_input)
    return response.text


def print_slowly(text: str, delay: float = 0.0002) -> None:
    for char in text:
        print(char, end="", flush=True)
        time.sleep(random.normalvariate(delay, delay / 10))


clear_screen()

while True:
    kill_flag = False
    user_input = input("> ")
    # Generate gibberish
    gibberish_length = random.randint(50, 2000)
    gibberish = generate_gibberish(gibberish_length)

    try:
        # Start Gemini response fetching in a separate thread
        gemini_response = get_gemini_response(user_input)
        # replace linebreaks with spaces
        gemini_response = gemini_response.replace("\n", " ")
    except Exception as e:  # noqa
        gemini_response = "...I ...I have  to go... Do...    not...  sleep..."
        kill_flag = True

    # Print slowly
    print_slowly(
        generate_gibberish(random.randint(50, 2000)),
        delay=0.003,
    )
    time.sleep(random.uniform(0.1, 0.6))
    print_slowly(gemini_response, delay=0.03)
    time.sleep(random.uniform(0, 0.2))
    print_slowly(
        generate_gibberish(random.randint(0, 200)),
        delay=random.uniform(0.001, 0.005),
    )
    if kill_flag:
        time.sleep(1.2)
        exit()
    print()
