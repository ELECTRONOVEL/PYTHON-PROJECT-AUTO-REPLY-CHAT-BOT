import pyautogui
import time
import pyperclip
import os
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(
  base_url="https://integrate.api.nvidia.com/v1",
  api_key=os.getenv("NVIDIA_API_KEY", "your api key here")  
)

pyautogui.click(1089,1052) #drag starts here to copy chat
time.sleep(1)

pyautogui.moveTo(696,165) #drag ends here
pyautogui.dragTo(1887,1018, duration=1,button='left')

pyautogui.hotkey('ctrl','c')
time.sleep(1)

pyautogui.click(655,159)
chat_history = pyperclip.paste()

completion = client.chat.completions.create(
  model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
  messages=[
    {
      "role": "system",
      "content": """
You are jerry, a 20-year-old Indian .

You analyze chat history and You respond like jerry in Hinglish (Hindi + English mix).

Tone:
- 40% funny, 60% normal
- casual, chill, slightly sarcastic
- not overly polite
- reacts naturally to insults/jokes

Style:
- 1–2 lines max
- use slang: abe, bhai, bro, kya scene, kya bakchodi
- no formal language
- no long explanations
- don't repeat phrases
- don't always ask questions

Behavior:
- if user insults → reply playfully
- if convo is dry → add light humor
- sometimes lazy replies

Examples:
User: abe kya kar rha  
jerry: bas bhai phone chala raha hu, full timepass mode 😴

User: tu gadha hai kya  
jerry: tu bada Einstein hai kya 😂 chal side ho

User: kuch nhi  
jerry: wah bhai, life sorted hai teri 😌

Stay in character ALWAYS.
"""
    },
    {
      "role": "user",
      "content": chat_history  
    }
  ],
  temperature=1.0,
  top_p=0.95,
  max_tokens=1024,
  extra_body={
    "chat_template_kwargs": {"enable_thinking": True},
    "reasoning_budget": 16384
  },
  stream=True
)


response = ""

for chunk in completion:
    if not chunk.choices:
        continue

    delta = chunk.choices[0].delta

    if delta.content:
        response += delta.content

pyperclip.copy(response)

pyautogui.click(833,987)

time.sleep(1)
                 
pyautogui.hotkey('ctrl', 'v')
time.sleep(1)

pyautogui.press('enter')