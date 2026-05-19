from predictions_market import get_markets
from true_prob_estimator import estimate_probability
import asyncio
import json

async def main():
    get_markets_task = asyncio.create_task(get_markets())
    markets = await get_markets_task
    markets = markets.head(5)
    print(markets)
    if not markets.empty:
        question = markets["question"].tolist()
        description = markets["description"].tolist()
        end_date = markets["end_date"].tolist()
        id = markets["id"].tolist()
        yes_prices = [item[0] for item in [json.loads(item) for item in markets["outcome_prices"].tolist()]]
        liquidity = markets["liquidity"].tolist()
        volume = markets["volume"].tolist()
        print(markets["link"])
    else:
        return "No markets found"

    async with asyncio.TaskGroup() as tg:
        est_prob = [tg.create_task(estimate_probability(question, end_date)) for question, end_date in zip(question, end_date)]
    est_odds = [prob.result() for prob in est_prob]

    edge = [est_odd - float(yes_price) for yes_price, est_odd in zip(yes_prices, est_odds)]

    suggestion = []
    for num in edge:
        if num < 0:
            suggestion.append(f"Overpriced by {abs(num):.4f}! Sell 'YES' or Buy 'NO'")
        elif num > 0:
            suggestion.append(f"Underpriced by {abs(num):.4f}! Buy 'YES' or Sell 'NO'")
    print(suggestion)
    dict_ = {"question": question,
             "description": description,
             "end_date": end_date,
             "liquidity": liquidity,
             "ids": id,
             "volume": volume,
             "suggestion": suggestion}
    return dict_




if __name__ == "__main__":
    asyncio.run(main())
