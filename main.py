import os
from dotenv import load_dotenv
from google import genai
import sys


def generate_content(client, prompt):
    return client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents= prompt
    )


def main():
    prompt = " ".join(sys.argv[1:]).strip()
    if not prompt:
        print("Please enter a prompt")
        sys.exit(1)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = generate_content(client, prompt)
    print(response.text)
    print(
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
        f"Response tokens: {response.usage_metadata.candidates_token_count}"  
    )


if __name__ == "__main__":
    main()
