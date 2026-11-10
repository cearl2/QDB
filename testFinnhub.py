import finnhub
finnhub_client = finnhub.Client(api_key="dbpdib9r01qvflacjf20dbpdib9r01qvflacjf2g")

print(finnhub_client.symbol_lookup('apple'))