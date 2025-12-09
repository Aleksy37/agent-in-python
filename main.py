import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="AI agent CLI tool")
    parser.add_argument("prompt", type=str, help="The user's prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable Verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY env var not set")

    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)])
    ]
    if args.verbose:
        print(f"User prompt: {args.prompt}\n")

    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    counter = 0
    while counter < 20:
        counter += 1
        function_responses = []
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
        except ConnectionError as e:
            print(f"Gemini API error:{e}")
            continue

        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")
        
        if verbose:
            print(
                f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
                f"Response tokens: {response.usage_metadata.candidates_token_count}"  
            )

        if not response.function_calls and response.text:
            print("Response:")
            print(response.text)
            break

        else:
            for candidate in response.candidates:
                messages.append(candidate.content)

            try:
                for function_call_part in response.function_calls:
                    result = call_function(function_call_part)
                    function_responses.append(result.parts[0])

                    if verbose:
                        tool_response = result.parts[0].function_response.response
                        result_text = tool_response.get("result", "")
                        print("->")
                        print(result_text)
                        
            except TypeError as e:
                print(f"Malformed response object: {e}") 

            messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
