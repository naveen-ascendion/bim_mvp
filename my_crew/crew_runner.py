from my_crew.my_agents import (
    SentimentAgent,
    ThemeClassifierAgent,
    PricingAgent,
    IssueSizingAgent,
    SellThroughAgent,
    ReportWriterAgent
)
from my_crew.my_tasks import (
    sentiment_task,
    theme_classification_task,
    pricing_analysis_task,
    issue_sizing_task,
    sell_through_task,
    report_writer_task
)
from crewai import Crew
from datetime import datetime
import json
import re
import os

def save_report(report_data: dict) -> str:
    date_str = datetime.now().strftime("%d-%m-%Y")
    os.makedirs("weekly_reports", exist_ok=True)

    if "generated_at" not in report_data:
        report_data["generated_at"] = datetime.now().isoformat()
    if "report_date" not in report_data:
        report_data["report_date"] = date_str

    filepath = os.path.join("weekly_reports", f"{date_str}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    return filepath

def run_crew() -> dict:
    crew = Crew(
        agents=[
            SentimentAgent,
            ThemeClassifierAgent,
            PricingAgent,
            IssueSizingAgent,
            SellThroughAgent,
            ReportWriterAgent
        ],
        tasks=[
            sentiment_task,
            theme_classification_task,
            pricing_analysis_task,
            issue_sizing_task,
            sell_through_task,
            report_writer_task
        ],
        verbose=True
    )

    result = crew.kickoff()
    output = getattr(result, "output", str(result)).strip()

    try:
        if output.startswith("{") or output.startswith("["):
            report_data = json.loads(output)
        else:
            json_match = re.search(r'\{.*\}', output, re.DOTALL)
            if json_match:
                report_data = json.loads(json_match.group())
            else:
                report_date = {
                    "raw_output": output,
                    "generated_at": datetime.now().isoformat()
                }

    except json.JSONDecodeError:
        report_data = {
            "raw_output": output,
            "generated_at": datetime.now().isoformat(),
            "note": "Output was not in JSON format, stored as raw text."
        }
    
    return report_data

if __name__ == "__main__":
    print("\nStarting crew execution...\n")
    report_data = run_crew()
    print("\n" + "="*50 + "\n")
    print("Crew execution successful.\n")
    filepath = save_report(report_data)
    print(f"Report saved at: {filepath}")
