import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("Couldn't find OpenAI Router Key")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    for _ in range(20):
        
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        if response.usage is None:
            raise RuntimeError("Failed API request, try again")

        message = response.choices[0].message
        messages.append(message)
        if not message.tool_calls:
            print(message.content)
            break
        if args.verbose: 
            print("User prompt: ", args.user_prompt)
            print("Prompt tokens: ", response.usage.prompt_tokens)
            print("Response tokens: ", response.usage.completion_tokens)
        # print("Response:\n", response.choices[0].message.content)

        for tool_call in response.choices[0].message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if result_message["content"] == "":
                raise Exception(f"Error: Something went wrong")
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
    else:
        print("...ran out of iterations...")
        sys.exit(1)
            

if __name__ == "__main__":
    main()
