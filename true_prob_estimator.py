from dotenv import load_dotenv
from groq import AsyncGroq
import os
import asyncio

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = AsyncGroq(api_key=GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"

async def estimate_probability(question, end_date):
    prompt = f"""
        You are an expert prediction market forecaster.
        Estimate the true probability (real number between 0 and 1) that this event will happen.
    
        Question: {question}
        End date: {end_date}
    
        Think step-by-step but return ONLY the final number, no extra texts. Don't hallucinate.
        Adhere to my instructions strictly.
        """
    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": "you are an expert analyst"}
                ,{"role": "user", "content": prompt}],
            temperature=0.0,      # Maximum consistency
            max_tokens=20,
        )

        prob = float(response.choices[0].message.content)

        print(f"   🚀 Groq ({MODEL}): {prob:.1%} → {question[:55]}...")
        return prob

    except Exception as e:
        print(f"   ⚠️ Groq error: {e}")
        return 0.50





















# groq_client = OpenAI(
#     api_key=GROQ_API_KEY,
#     base_url="https://api.groq.com/openai/v1",
# )
# response = groq_client.responses.create(
#     input= prompt,
#     model="openai/gpt-oss-20b",
# )
# print(response.output_text)






# response = gemini_client.models.generate_content(
#     model="gemini-3-flash-preview", contents='''what do you think the right odds for this prediction market should be:
# strait-of-hormuz-traffic-returns-to-normal-by-may-15? provide only the figures,
# no additional text. I want to pass your response into a program that calculates
# '''
# )
# print(response.text)