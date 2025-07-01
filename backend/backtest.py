
import argparse

import pandas as pd

from backend.agents.top_agents import (
    PredictiveProphetAgent,
    QuantumBoostAgent,
    VWAPScalperXAgent,
)

def main(agent_name, data_path):
    df = pd.read_csv(data_path)
    agents = {
        "QuantumBoost": QuantumBoostAgent(),
        "PredictiveProphet": PredictiveProphetAgent(None),
        "VWAPScalperX": VWAPScalperXAgent(),
    }
    agent = agents[agent_name]
    trades, pnl = 0, 0
    for i in range(201, len(df)):
        action, conf = agent.signal(df.iloc[:i])
        if action == "BUY":
            trades += 1
            pnl += (df['close'].iloc[i] - df['close'].iloc[i-1])
    print(f"Agent: {agent_name} | Trades: {trades} | PnL: {pnl:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", type=str, required=True)
    parser.add_argument("--data", type=str, required=True)
    args = parser.parse_args()
    main(args.agent, args.data)

