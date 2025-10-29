async def analyze_bill(bill_amount: float, rate_per_kwh: float):
    # Calculate kWh used
    kwh_used = bill_amount / rate_per_kwh if rate_per_kwh else 0
    prompt = f"""
The company KPLC bill for the previous month was KES {bill_amount:,.2f}.
The rate per kWh is KES {rate_per_kwh:,.2f}.
This means the company used {kwh_used:,.2f} kWh.

Analyze whether this usage is efficient for a typical company, suggest possible reasons for high/low usage, and recommend actions to improve efficiency. Give actionable insights for a company admin in Kenya."
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    return content.strip() if content else "No analysis returned."
# services/ai_analytics_service.py
import os
import groq

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=GROQ_API_KEY)

MODEL_NAME = "groq/compound-mini"  # or whatever is available

ANALYSIS_SYSTEM_PROMPT = """
You are an energy analytics assistant. Analyze the provided department or company energy metrics. Focus on expected_daily, expected_monthly, and deviation. Give actionable insights, highlight anomalies, and suggest improvements. Ignore overtime_monthly and waste_monthly.
"""

def build_prompt(metrics, name="Department"):
    return f"""
Analyze the following metrics for {name}:

Expected Daily: {metrics.get('expected_daily', {})}
Expected Monthly: {metrics.get('expected_monthly', {})}
Deviation: {metrics.get('deviation', {})}
"""

async def analyze_department(department: dict):
    metrics = department.get("metrics", {})
    prompt = build_prompt(metrics, name=department.get("name", "Department"))
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    return content.strip() if content else "No analysis returned."

async def analyze_company(departments: list):
    summary = ""
    for dept in departments:
        metrics = dept.get("metrics", {})
        summary += f"Department: {dept.get('name', 'Unknown')}\n"
        summary += f"Expected Daily: {metrics.get('expected_daily', {})}\n"
        summary += f"Expected Monthly: {metrics.get('expected_monthly', {})}\n"
        summary += f"Deviation: {metrics.get('deviation', {})}\n\n"
    prompt = f"Analyze the following company-wide metrics (all departments):\n\n{summary}"
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    return content.strip() if content else "No analysis returned."
