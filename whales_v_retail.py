from predictions_market import get_markets
import asyncio
import httpx




holders_url = "https://data-api.polymarket.com/holders"

async def get_whales(link):
    slug = link.replace("https://polymarket.com/event/", '').split("#")[0]
    client = httpx.Client()
    response = client.get(f"https://gamma-api.polymarket.com/events/slug/{slug}")
    event = response.json()
    market_details = event["markets"]
    questions = []
    condition_id = []
    for market in market_details:
        questions.append({market["conditionId"]: market["question"]})
        condition_id.append(market["conditionId"])

    params = {"market": condition_id[:20],
              "limit": 20,
              "minBalance": 1000}
    async with httpx.AsyncClient() as client:
        response =  await client.get(holders_url, params=params)
        # token_type_task = asyncio.create_task(client.get(f"https://clob.polymarket.com/markets-by-token/{token_id}"))
        data = response.json()
    feedback = []
    for item in data:
        feedback.append({"token": item["token"],
                    "no_of_holders": len(item["holders"]),
                    "outcome": "Yes" if item["holders"][0]["outcomeIndex"] == 0 else "No",
                    "message": f"The market with token: {item["token"]}, has {len(item["holders"])} whales buying {"Yes" if item["holders"][0]["outcomeIndex"] == 0 else "No"}"})


    return feedback

if __name__ == "__main__":
    asyncio.run(get_whales("https://polymarket.com/event/pga-championship-winner-2026#XgtzIgAD"))
