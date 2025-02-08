import time
import os
from openai import OpenAI

client = OpenAI(
    api_key="s5fd25",
    base_url="https://api.vsegpt.ru/v1",
)

PROMPT_FILE = "/home/handbook/test.txt"
COMMAND_QUIT = "n"
COMMAND_RUN = "y"

def read_prompt():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def send_request(prompt):
    messages = [{"role": "user", "content": prompt}]
    response_big = client.chat.completions.create(
        model="deepseek/deepseek-chat-alt",
        messages=messages,
        temperature=0.3,
        n=1,
        max_tokens=5000,
    )
    return response_big.choices[0].message.content

def main():
    while True:
        command = input("Введите команду (run для запроса, exit для выхода): ").strip().lower()
        
        if command == COMMAND_QUIT:
            print("Выход из программы...")
            break
        elif command == COMMAND_RUN:
            prompt = read_prompt()
            if prompt:
                
                print("Отправка запроса...")
                response = send_request(prompt)
                print("Ответ:", response)
            else:
                print("Файл пуст или отсутствует. Введите запрос в", PROMPT_FILE)
        else:
            print("Неизвестная команда. Введите 'run' или 'exit'.")

if __name__ == "__main__":
    main()
