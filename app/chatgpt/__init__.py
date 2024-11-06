from openai import OpenAI
from flask import current_app

api_key = current_app.config['OPENAI_API_KEY']

client = OpenAI(api_key=api_key)


def check_comment(ai_conditions, content):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"You are a helpful assistant for checking comment for hate speech, toxicity, obscenity, threats, insults, name calling, shaming or bullying. And also for checking comment for conformity with the next conditions: {ai_conditions}. If the comment satisfies the conditions, you will respond with 'True'. If the comment does not satisfy the conditions, you will respond with 'False' and the reason why."},
        {
            "role": "user",
            "content": f"{content}"
        }
        ]
        )

    print(completion.choices[0].message)
    return completion.choices[0].message
        

