# import os
# import json
# import asyncio
# from datetime import datetime
# from pathlib import Path
# from dotenv import load_dotenv
# from groq import AsyncGroq
#
# load_dotenv()
#
# question = ''' will arsenal win the premier league? '''
# end_date = '2026-6-6'
# # ========================= CONFIG =========================
# CACHE_FILE = Path("prob_cache.json")
# CACHE_EXPIRY_DAYS = 14
#
# client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
#
# MODEL = "llama-3.3-70b-versatile"   # Best balance of speed + reasoning
# # MODEL = "llama-3.1-8b-instant"    # Ultra fast fallback if you hit limits
#
# # Load/save cache
# def load_cache():
#     if CACHE_FILE.exists():
#         try:
#             with open(CACHE_FILE, "r") as f:
#                 return json.load(f)
#         except:
#             return {}
#     return {}
#
# def save_cache(cache):
#     with open(CACHE_FILE, "w") as f:
#         json.dump(cache, f, indent=2)
#
# cache = load_cache()
#
# # =======================================================
#
# async def estimate_true_prob(question: str, end_date: str = None) -> float:
#     """Async Groq probability estimator with caching."""
#     cache_key = f"{question}|{end_date or ''}".strip()
#
#     # Return cached result if fresh
#     if cache_key in cache:
#         cached = cache[cache_key]
#         days_old = (datetime.now() - datetime.fromisoformat(cached["timestamp"])).days
#         if days_old < CACHE_EXPIRY_DAYS:
#             prob = cached["probability"]
#             print(f"   📋 Cache hit: {prob:.1%} → {question[:55]}...")
#             return prob
#
#     # New estimation
#     prob = await _get_groq_probability(question, end_date)
#
#     # Save to cache
#     cache[cache_key] = {
#         "probability": prob,
#         "timestamp": datetime.now().isoformat(),
#         "question": question
#     }
#     save_cache(cache)
#
#     return prob
#
#
# async def _get_groq_probability(question: str, end_date: str = None) -> float:
#     """Core async Groq call."""
#     prompt = f"""
# You are a world-class prediction market forecaster.
# Estimate the true probability (as integer 0-100) that this event happens.
#
# Question: {question}
# End date: {end_date or 'Unknown'}
#
# Reply with ONLY a valid JSON object like this: {{"probability": 65}}
# No explanation. No extra text.
# """
#
#     try:
#         response = await client.chat.completions.create(
#             model=MODEL,
#             messages=[{"role": "system", "content": "you are an expert analyst"}
#                 ,{"role": "user", "content": prompt}],
#             temperature=0.0,      # Maximum consistency
#             max_tokens=20,
#         )
#
#         content = response.choices[0].message.content.strip()
#         result = json.loads(content)
#         prob = int(result["probability"]) / 100.0
#         prob = max(0.01, min(0.99, prob))
#
#         print(f"   🚀 Groq ({MODEL}): {prob:.1%} → {question[:55]}...")
#         return prob
#
#     except Exception as e:
#         print(f"   ⚠️ Groq error: {e}")
#         return 0.50

string = "https://polymarket.com/event/pga-championship-winner-2026#XgtzIgAD"

new_string = string.lstrip("https://polymarket.com/event/").split("#")[0]
print(new_string)