from google import genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)


def get_resume_tip(role, skills):
    prompt = (
        f"Give 5 concise, actionable resume tips for a fresher applying "
        f"for a {role} role. Their skills: {skills}. "
        f"Keep it under 150 words."
    )
    response = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt,
    )
    return response.text