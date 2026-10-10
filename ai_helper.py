import time

from google import genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

# Tried in order. The first one that answers wins.
MODELS = [
    config.GEMINI_MODEL,
    "gemini-3-flash-preview",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]


def get_resume_tip(role, skills):
    prompt = (
        f"Give 5 concise, actionable resume tips for a fresher applying "
        f"for a {role} role. Their skills: {skills}. "
        f"Use plain text only, numbered 1 to 5, with no markdown symbols "
        f"such as asterisks. Keep it under 150 words."
    )

    last_error = None
    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            last_error = e
            print(f"Gemini error ({model}):", e)
            time.sleep(1)
    raise last_error