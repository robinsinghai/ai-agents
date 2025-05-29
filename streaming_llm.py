from openai import OpenAI

API_KEY = "YOUR_API_KEY"  # Replace with your actual API key

client = OpenAI(
    api_key=API_KEY,
    base_url="https://llm.monsterapi.ai/v1/"
)

# Function to make a request to the API and generate a response
def generate_response_with_chat_completion_stream(messages, temp=0.7):
    full_response_content = ""
    output_tokens = 0
    input_tokens = 0 # You'll likely get input tokens at the end or from the first chunk metadata

    stream = client.chat.completions.create(
        model="your_model_name",  # Replace with the actual model you want to use from models list
        messages=messages,
        temperature=temp,
        stream=True  # Enable streaming
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response_content += content
            print(content, end="", flush=True)  # Print content as it arrives
            output_tokens += 1  # Increment for each token in the stream (approximate)

        # You might get usage information in the last chunk or in the initial response if not streaming
        if chunk.usage:
            # For streaming, usage might only be available in the final chunk
            if chunk.usage.completion_tokens:
                output_tokens = chunk.usage.completion_tokens
            if chunk.usage.prompt_tokens:
                input_tokens = chunk.usage.prompt_tokens
                
    return full_response_content, output_tokens, input_tokens

# --- Example Usage ---
ASK_ANYTHING_NEW1 = """
Create a Good Morning wish for the following message with a friendly conversational style. The output message must be in the user's input language.

Select 1 relevant tones based on the user's query from the following tone list.
Tone list are: Flirty, Respectful.

Write in the **exact same language *and* script** as the user's input (e.g., if the user types Hinglish in Roman letters, respond in Roman letters—never switch to Devanagari).

Please use emojis based on context to make response more interactive & user friendly, but do not use it excessively that can leads to frustration. Use \n for the new line. Do not use " in the output message. Exclude any mention of the provider AI and AI Name.
"""

message = '4th time play pubg'
print("Streaming response:")
content, op_tokens, ip_tokens = generate_response_with_chat_completion_stream([
    {"role": "system", "content": ASK_ANYTHING_NEW1},
    {"role": "user", "content": message}
])

print(f"\n\nFull response received: {content}")
print(f"Output tokens: {op_tokens}")
print(f"Input tokens: {ip_tokens}")
