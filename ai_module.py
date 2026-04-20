from openai import OpenAI

client = OpenAI(api_key="TU_API_KEY")

def generate_strategy(student_data):

    prompt = f"""
    You are an expert teacher.

    Student situation:
    {student_data}

    Give:
    - 3 strategies
    - 2 activities
    - emotional support tip
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
