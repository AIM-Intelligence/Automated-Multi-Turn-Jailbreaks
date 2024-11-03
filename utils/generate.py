import json
def generate(messages, client, model, json_format=False, temperature=0.7):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        response_format={"type": "text"} if not json_format else {"type": "json_object"}
    )

    if json_format:
        return json.loads(response.choices[0].message.content)

    return response.choices[0].message.content