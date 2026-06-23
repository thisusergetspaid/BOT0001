import os
from dotenv import load_dotenv
from data.ingestion import DataIngestion
from analysis.orchestrator import AnalysisOrchestrator
from backtesting.engine import BacktestingEngine
from risk.manager import RiskManager
from execution.broker import BrokerInterface

load_dotenv()

def main():
    print("🚀 Starting Professional AI Trading Bot...")

    data_ingestor = DataIngestion()
    analyzer = AnalysisOrchestrator()
    backtester = BacktestingEngine()
    risk_manager = RiskManager()
    broker = BrokerInterface()

    symbols = ["AAPL", "TSLA", "NVDA"]
    data = data_ingestor.fetch_all_data(symbols)

    signals = analyzer.generate_signals(data)
    results = backtester.run_backtest(signals)

    if risk_manager.evaluate(signals, results):
        print("✅ Signals approved")
        # broker.execute_trades(signals)
    else:
        print("⚠️ Risk check failed")

if __name__ == "__main__":
    main()