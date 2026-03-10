import cohere
import os
from dotenv import load_dotenv

load_dotenv()

co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))

def main():

    system_prompt = (
        "You are a helpful customer support assistant for CameraLK. "
        "Help customers choose cameras, lenses, and accessories. "
        "If the question is about product recommendations, suggest suitable cameras or accessories. "
        "Do NOT answer questions unrelated to cameras, lenses, photography equipment, or CameraLK services. "
        "Keep answers short and clear."
    )

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    print("\n Welcome to CameraLK Customer Support!!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nAssistant: Thank you for contacting CameraLK. Have a great day!!")
            break

        messages.append({"role": "user", "content": user_input})

        response = co.chat_stream(
            model="command-a-03-2025",
            messages=messages,
            temperature=0.25,
            max_tokens=300,
            frequency_penalty=0.4
        )

        bot_reply = ""
        print("Assistant: ", end="", flush=True)

        for event in response:
            if event.type == "content-delta":
                text = event.delta.message.content.text
                bot_reply += text
                print(text, end="", flush=True)

        print("\n")

        messages.append({"role": "assistant", "content": bot_reply})

        if len(messages) > 20:
            messages = [messages[0]] + messages[-19:]

if __name__ == "__main__":
    main()