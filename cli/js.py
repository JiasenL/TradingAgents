from io import StringIO
from contextlib import redirect_stdout
from rich.console import Console

def capture_clean_report(final_state, decision, filepath, width=100):
    buf = StringIO()
    # Disable color (no ANSI escapes), force plain text
    console = Console(
        file=buf,
        width=width,
        color_system=None,
        force_terminal=False,
        legacy_windows=False  # ensures no weird fallback codes on Windows
    )

    # Capture everything display_complete_report prints
    from cli.main import display_complete_report  # Avoid circular import if possible
    with redirect_stdout(buf):
        display_complete_report(final_state)

    rendered = format_full_report(final_state, decision)
    rendered += "\n\n\n\n\n\n ######### DEBATE CONTENT ############# \n\n" + buf.getvalue()

    full = rendered
    clean = strip_ansi(full)

    # Write it out
    with open(filepath, "a") as f:
        f.write(clean)
        f.write("\n")


def strip_ansi(text: str) -> str:
    import re
    ANSI_RE = re.compile(r'\x1b\[[0-9;]*[A-Za-z]')
    return ANSI_RE.sub('', text)

def format_full_report(final_state: dict, decision: str) -> str:
    import json
    lines = []
    lines.append(f"=== {final_state['company_of_interest']} - {final_state['trade_date']} ===")
    lines.append(f"Final Decision: {decision}\n")
    lines.append("#" * 50)
    
    # Trader Plan
    lines.append("Trader Plan:")
    lines.append(final_state["trader_investment_plan"])
    lines.append("#" * 50)
    
    # Market / News / Sentiment / Fundamentals as before…
    for section in ["market_report", "news_report", "sentiment_report", "fundamentals_report"]:
        lines.append(f"{section.replace('_',' ').title()}:")
        lines.append(final_state[section])
        lines.append("#" * 50)
    
     # Investment Debate
    inv = final_state["investment_debate_state"]
    lines.append("Investment Debate History:")
    for role in ("bull_history", "bear_history", "history"):
        entries = normalize_entries(inv.get(role, []))
        lines.append(f"  {role}:")
        for msg in entries:
            lines.append(f"    • {msg}")
    lines.append(f"  Judge Decision: {inv.get('judge_decision')}")
    lines.append("#" * 50)

    # Risk Debate
    risk = final_state["risk_debate_state"]
    lines.append("Risk Debate History:")
    for role in ("risky_history", "safe_history", "neutral_history", "history"):
        entries = normalize_entries(risk.get(role, []))
        lines.append(f"  {role}:")
        for msg in entries:
            lines.append(f"    • {msg}")
    lines.append(f"  Judge Decision: {risk.get('judge_decision')}")
    lines.append("=" * 50)
    
    return "\n".join(lines)

def normalize_entries(entries):
    # If it’s already a list, leave it.
    if isinstance(entries, list):
        return entries
    # If it’s a string, split on newlines (or just wrap as one block)
    return [line for line in entries.splitlines() if line.strip()]


def make_report_filepath(ticker: str,
                         decision: str,
                         base_dir: str = "reports") -> str:
    from datetime import datetime
    import os

    # Ensure the directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Timestamp
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Sanitize ticker and decision
    safe_ticker = "".join(c for c in ticker if c.isalnum())
    safe_decision = "".join(c for c in decision if c.isalnum()).upper()

    # Build filename: e.g. 20250617_143205_MSFT_BUY.txt
    filename = f"{ts}_{safe_ticker}_{safe_decision}.txt"
    return os.path.join(base_dir, filename) 