import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
import sys
from prompts import system_prompt


def generate_content(client, messages):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents= messages,
        config= types.GenerateContentConfig(system_instruction=system_prompt)
    )


def main():
    parser = argparse.ArgumentParser(description="AI agent CLI tool")
    parser.add_argument("prompt", type=str, help="The user's prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable Verbose output")
    args = parser.parse_args()
    prompt = args.prompt
    verbose = args.verbose
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Gemini api key not set in environment")
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    if verbose:
        print(f"User prompt: {prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text   =prompt)])
    ]

    response = generate_content(client, messages)

    print(response.text)

    if verbose:
        print(
            f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
            f"Response tokens: {response.usage_metadata.candidates_token_count}"  
        )


if __name__ == "__main__":
    main()
