from groq import Groq

from bot.config import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)


async def generate_study_plan(
    subject: str,
    exam_date: str,
    daily_hours: int
):

    prompt = f"""
                You are an AI study planner.

                Create a realistic study plan.

                Subject:
                {subject}

                Exam date:
                {exam_date}

                Available study time:
                {daily_hours} hours per day


                Requirements:
                - Split the plan into weeks.
                - Add topics to learn.
                - Add practice tasks.
                - Add revision days.
                - Keep it realistic.
                - Answer only in English.
            """


    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content