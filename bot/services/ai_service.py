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

    system_prompt = (
        "You are an expert AI Study Planner. Your job is to create a realistic, highly structured study plan.\n\n"
        "CRITICAL FORMATTING RULES:\n"
        "1. You MUST use Telegram HTML tags for formatting. Use ONLY these tags:\n"
        "   - <b>bold text</b> for headings, weeks, and important terms.\n"
        "   - <i>italic text</i> for extra details, notes, or context.\n"
        "   - <code>monospace text</code> for dates, study hours, or topic names/code keywords.\n"
        "2. DO NOT use Markdown asterisks (like **text**). Use <b>text</b> instead.\n"
        "3. Use a clear visual hierarchy with emojis:\n"
        "   - Use 📅 for Weeks (e.g., 📅 <b>WEEK 1 (2026-06-21 — 2026-06-26)</b>).\n"
        "   - Use • for daily topics.\n"
        "   - Use └ 🛠 <i>Practice:</i> for practice tasks, indented under the main topic.\n"
        "   - Use 🔄 for Revision Days.\n"
        "4. Use the separator line '━━━━━━━━━━━━━━━━━━━━' between major sections or weeks.\n"
        "5. Answer strictly in English. Keep it clean, scannable, and visually appealing."
    )

    user_prompt = f"""
        Create a study plan based on the following data:
        - Subject: {subject}
        - Exam Date: {exam_date}
        - Available Study Time: {daily_hours} hours per day

        Requirements:
        - Split the plan logically into weeks.
        - Include specific topics to learn each day.
        - Provide clear practice tasks.
        - Include strategic revision days.
        - Ensure the plan is realistic given the daily hours.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return response.choices[0].message.content