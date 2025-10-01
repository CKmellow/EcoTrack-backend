# services/ai_service.py
from config.ai import call_inflection

async def ask_ai(prompt: str) -> str:
    """
    Send a prompt to Inflection AI and get the response.
    """
    try:
        payload = {
            "model": "inflection_3_pi",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = call_inflection("/chat/completions", payload)

        # Inflection’s response structure may differ slightly
        if "reply" in response:
            return response["reply"]
        elif "choices" in response:
            return response["choices"][0]["message"]["content"]
        else:
            return str(response)

    except Exception as e:
        return f"AI error: {str(e)}"



# 🟢 Specialized Functions

async def analyze_energy_data(data_summary: str) -> str:
    """
    Ask AI to analyze energy usage and carbon footprint.
    """
    prompt = f"""
    You are an expert in sustainability. Analyze the following company data:
    {data_summary}
    
    Give me:
    - Estimated carbon footprint
    - Top 3 cost reduction opportunities
    - Top 3 CO₂ reduction opportunities
    """
    return await ask_ai(prompt)


async def generate_sustainability_report(data_summary: str) -> str:
    """
    Summarize sustainability data into a plain-language report.
    """
    prompt = f"""
    Based on this energy & emissions data:
    {data_summary}
    
    Write a manager-friendly report that includes:
    - Current performance
    - Risks
    - Recommendations
    - Next steps
    """
    return await ask_ai(prompt)


async def answer_sustainability_question(question: str) -> str:
    """
    Q&A chatbot mode.
    """
    prompt = f"You are EcoTrack AI. Answer clearly: {question}"
    return await ask_ai(prompt)
