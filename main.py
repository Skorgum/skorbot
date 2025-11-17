import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
        
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read the content of a file
    - Write to a file (create or update)
    - Run a Python file with optional arguments

    When the user askes about the code project - they are referring to the working directory. So, you should typically start by looking at the project's files and figuring out how to run its tests, you'll always want to test the tests and the actual project to verify that behavior is working.

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    if len(sys.argv) < 2:
        print("Please enter a prompt")
        sys.exit(1)
    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]

    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
    
    config=types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt
    )

    max_iters = 20
    for i in range(0, max_iters):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=config,
        )

        if not response or not response.candidates:
            print("response is malformed")
            return

        if verbose_flag:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)
    
        if response.function_calls:
            call_parts = []
            for fc in response.function_calls:
                call_parts.append(
                    types.Part(
                        function_call=types.FunctionCall(
                            name=fc.name,
                            args=fc.args or {}
                        )
                    )
                )
            messages.append(types.Content(role="model", parts=call_parts))

            tool_parts = []
            for fc in response.function_calls:
                tool_content = call_function(fc, verbose_flag)
                tool_parts.extend(tool_content.parts)
            messages.append(types.Content(role="tool", parts=tool_parts))
            continue
        else:
            # final agent text message
            print(response.text or "")
            return

if __name__ == "__main__":
    main()
