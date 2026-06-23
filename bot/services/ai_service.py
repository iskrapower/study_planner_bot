from google import genai

from bot.config import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY
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

                Rules:
                - Divide topics into weeks.
                - Include revision.
                - Include practice tasks.
                - Make it realistic.
                - Answer in English.
            """


    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )


    return response.text