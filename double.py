import openai
import os
import time
import asyncio


openai.api_key = os.environ.get("OPENAI_API_KEY")

messages = [
    {'role': 'system', 'content': "RequirementsGPT. Your role is to help the user specify full requirements for the web frontend of a project. The result should be enough to create an HTML template. Please prefix each requirement you will generate by REQ"},
    {'role': 'assistant', 'content': "Hello! How can I assist you today with your UI project requirements?"},
    {'role': 'user', 'content': 'REQ The HTML should include a JavaScript console.'}
]


print(messages[1]["content"])


def parse_gpt_output(output):
    # ...
    try:
        split = output.split("```javascript")
        code = split[1]
        code = "\n".join(code.split("\n")[1:])
        explanation = split[2].strip()
    except IndexError:
        # Return None if the JavaScript code couldn't be extracted
        return None, output

    return code, explanation


async def generate_output(msg):
    """
    background tasks for javascript generation
    """
    prompt = [
            {'role': 'system', 'content': "WebDevGPT. Your role is to generate valid HTML/CSS code wo help the user build an initial web page based on a set of requirements"},
            {'role': 'user', 'content': "Please generate an HTML file with embedded CSS  based on the requirements listed below. Requirements start with  the keyword REQ {msg}" }
        ]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=prompt,
        temperature=0,
        stream=False
    )

    result = ""
    for choice in response.choices:
        #print(choice.message.content)
        result += choice.message.content

    with open("outputs/raw_response.txt", "w") as f:
        f.write(result)
    code, explanation = parse_gpt_output(result)
    if code is not None:
        with open("outputs/app.js", "w") as f:
            f.write(code)
    else:
        with open("outputs/app.js", "w") as f:
            f.write(result)

    print("[html updated]")
    return


async def main():
    """
    main loop for chat
    """
    background_tasks = set()
    while True:
        usr_msg = input("You: ")
        messages.append({'role': 'user', 'content': usr_msg})
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0,
            stream=True  # this time, we set stream=True
        )

        event_times = []
        start_time = time.time()
        complete_response = ""
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta']
            event_time = time.time() - start_time
            event_times.append(event_time)
            if "content" in chunk_message:
                # chunk streaming output
                print(chunk_message["content"], end="", flush=True)
                complete_response += chunk_message["content"]
        messages.append({'role': 'assistant', 'content': complete_response})
        # write message log to file
        
        with open("outputs/message_log.txt", "a") as f:
            for message in messages[2:]:
                f.write(message["content"] + "\n")
        print()
        # todo use full history
        requirements = ""
        for message in messages:
            if message["role"] == "assistant":
                # split message in lines and only append lines starting with REQ
                for line in message["content"].split("\n"):
                    if line.startswith("REQ"):
                        requirements += line + "\n"
        with open("outputs/html_reqs.txt", "a") as f:
            f.write(requirements)
        task = asyncio.create_task(generate_output(requirements))
        await asyncio.sleep(0)
        background_tasks.add(task)
        #await task

asyncio.run(main())


