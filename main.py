from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Create a custom config
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "google"  # Use a different model
config["backend_url"] = "https://generativelanguage.googleapis.com/v1"  # Use a different backend
config["deep_think_llm"] = "gemini-2.0-flash"  # Use a different model
config["quick_think_llm"] = "gemini-2.0-flash"  # Use a different model
config["max_debate_rounds"] = 3  # Set desired debate rounds
config["online_tools"] = True  # Enable online tools

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# forward propagate
final_state, decision = ta.propagate("BA", "2025-06-16")
print(decision)

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns
# Save to file
# with open("trading_report.txt", "a") as f:
#     f.write(f"=== {final_state['company_of_interest']} - {final_state['trade_date']} ===\n")
#     f.write(f"Final Decision: {decision}\n")
#     f.write(f"Trader Plan: {final_state['trader_investment_plan']}\n")
#     f.write(f"Market Report: {final_state['market_report']}\n")
#     f.write(f"News Report: {final_state['news_report']}\n")
#     f.write(f"Sentiment Report: {final_state['sentiment_report']}\n")
#     f.write(f"Fundamentals Report: {final_state['fundamentals_report']}\n")
#     f.write("=" * 50 + "\n\n")