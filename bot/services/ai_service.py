import asyncio

from google import genai
from google.genai.errors import ServerError

from bot.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)



async def generate_study_plan(
    subject: str,
    exam_date: str,
    daily_hours: int
):

    prompt = f"""
                Create a study plan.

                Subject:
                {subject}

                Exam date:
                {exam_date}

                Daily study time:
                {daily_hours} hours.

                Requirements:
                - Split the plan into weeks.
                - Include learning topics.
                - Include practice.
                - Include revision.
                - Keep it realistic.
                - Answer in English.
            """


    retries = 3


    for attempt in range(retries):

        try:

            response = await client.aio.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            return response.text


        except ServerError as error:

            if attempt == retries - 1:
                raise error


            await asyncio.sleep(
                2 ** attempt
            )


    return "Could not generate plan."