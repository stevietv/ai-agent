import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import *

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("no API key found in .env file")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Users prompt for chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, 
            temperature=0,
            tools=[available_functions],
            )
    )    
    
    if response.usage_metadata == None:
        raise RuntimeError("no response received")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response:\n{response.text}")

    if response.function_calls:

        function_call_responses = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)

            if not function_call_result.parts:
                raise Exception("Unexpected response received")
            
            if not function_call_result.parts[0].function_response:
                raise Exception("No function call returned")

            if not function_call_result.parts[0].function_response.response:
                raise Exception("No function call response received")
            
            function_call_responses.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

if __name__ == "__main__":
    main()
