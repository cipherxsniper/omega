from gpt4all import GPT4All

model = GPT4All("ggml-gpt4all-j")

def ask_omega(prompt):
    with model.chat_session():
        return model.generate(prompt, max_tokens=200)

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        response = ask_omega(user_input)
        print("Omega:", response)
