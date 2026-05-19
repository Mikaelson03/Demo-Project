from datetime import datetime, timedelta
import httpx
import asyncio
import pandas as pd

today = datetime.now().date()
MIN_END_DATE = today + timedelta(days=1)
MAX_END_DATE = today + timedelta(days=7)

MIN_VOLUME = 50000
MIN_LIQUIDITY = 20000


gamma_url = "https://gamma-api.polymarket.com/markets"
gamma_params = {"liquidity_num_min": MIN_LIQUIDITY,
          "volume_num_min": MIN_VOLUME,
          "limit": 10,
          "ascending": True,
          "end_date_max": MAX_END_DATE,
          "end_date_min": MIN_END_DATE,
          }

market_details = []

async def get_markets():
    global market_details
    async with httpx.AsyncClient() as client:
        response = await client.get(gamma_url, params=gamma_params)
        data = response.json()

    for item in data:
        if item["outcomes"] != str(["Yes", "No"]):
            market_details.append({"id": item["id"],
                                   "question": item["question"],
                                   "description": item["description"],
                                   "outcomes": item["outcomes"],
                                   "outcome_prices": item["outcomePrices"],
                                   "token_ids": item["clobTokenIds"],
                                   "liquidity": item["liquidity"],
                                   "volume": item["volume"],
                                   "end_date": item["endDate"],
                                   "condition_id": item["conditionId"],
                                   "link": f"https://polymarket.com/event/{item["events"][0]["slug"]}",
                                   })
    df = pd.DataFrame(market_details)
    # print(market_details[0]["condition_id"])
    return df

if __name__ == "__main__":
    asyncio.run(get_markets())