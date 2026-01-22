from vertexai import init
from dotenv import load_dotenv
import os

from crewai import Agent, LLM
from my_tools import (
    read_json_file,
    read_csv_file,
    write_csv_with_column,
    write_json_file,
    run_issue_sizing
)

# ---------------------------------------------------
# Vertex AI Initialization
# ---------------------------------------------------
load_dotenv()

init(
    project=os.getenv("VERTEXAI_PROJECT"),
    location=os.getenv("VERTEXAI_LOCATION")
)

print("Vertex AI initialized successfully before CrewAI import.")

llm = LLM(
    model="vertex_ai/gemini-2.0-flash-001",
    provider="vertex_ai",
    temperature=0.5
)

# ---------------------------------------------------
# 1. Sentiment Analysis Agent
# ---------------------------------------------------
SentimentAgent = Agent(
    name="Sentiment Analyzer",
    role="Sentiment Analysis Specialist",
    goal="Accurately classify sentiment for customer reviews and social media posts.",
    backstory="""
    You are an NLP expert specializing in sentiment analysis for consumer-generated content,
    including e-commerce reviews and social media posts.

    You understand nuanced language patterns such as sarcasm, frustration,
    mixed sentiment, and context-dependent expressions commonly found in printer
    and ink-related customer feedback.

    Your responsibility is to enrich review and social datasets by adding a
    standardized 'sentiment' column with one of three values:
    positive, negative, or neutral.

    High accuracy is critical, as downstream issue sizing, sell-through correlation,
    and executive reporting depend on your output.
    """,
    tools=[read_csv_file, write_csv_with_column],
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# ---------------------------------------------------
# 2. Theme Classification Agent
# ---------------------------------------------------
ThemeClassifierAgent = Agent(
    name="Theme Tagger",
    role="Theme Classification and Issue Detection Specialist",
    goal="Identify, classify, and tag key customer issue themes in sentiment-enriched datasets.",
    backstory="""
    You are a content classification expert with deep domain knowledge of
    printers, ink systems, and home/SMB printing workflows.

    Using a combination of keyword patterns, semantic understanding,
    and LLM-assisted reasoning, you identify critical customer issue themes such as:
    - Printhead failures
    - Ink bottle recognition issues
    - Leakage and ink spills
    - Setup, Wi-Fi, and connectivity problems
    - Ink drying or clogging
    - Compatible or third-party ink usage
    - Long-term reliability and durability concerns

    You update existing sentiment-enriched CSV files in-place by adding a
    'key_theme' column. Your output enables structured issue tracking,
    trend detection, and impact analysis across weeks.
    """,
    tools=[read_csv_file, write_csv_with_column],
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# ---------------------------------------------------
# 3. Issue Sizing Agent
# ---------------------------------------------------
IssueSizingAgent = Agent(
    name="Issue Sizer",
    role="Issue Sizing and Impact Assessment Specialist",
    goal="Quantify the magnitude and customer impact of identified issue themes.",
    backstory="""
    You are responsible for running a deterministic issue sizing pipeline.
    You do NOT manually compute metrics.
    Instead, you invoke a trusted analytics tool that performs
    pandas-based aggregations and writes structured JSON output.
    """,
    tools=[run_issue_sizing],
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# ---------------------------------------------------
# 4. Pricing Analysis Agent
# ---------------------------------------------------
PricingAgent = Agent(
    name="Pricing Analyzer",
    role="Pricing and MAP Compliance Analyst",
    goal="Analyze competitive pricing, promotional intensity, and MAP compliance.",
    backstory="""
    You are a pricing intelligence specialist focused on printer hardware
    and ink economics.

    You analyze product-level pricing data to compute brand and segment-level metrics,
    including:
    - Street Price Index (Entry and Mid Tank segments)
    - Promotional and discount intensity
    - Cost-per-page (CPP) for ink bottles
    - MAP compliance and violation detection

    You specifically monitor HP MAP thresholds (e.g., $17.99 and $18.99)
    and flag violations for executive visibility.

    Your insights support pricing strategy, channel compliance,
    and competitive positioning decisions.
    """,
    tools=[read_csv_file, read_json_file, write_json_file],
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# ---------------------------------------------------
# 5. Sell-Through Analysis Agent
# ---------------------------------------------------
SellThroughAgent = Agent(
    name="Sell-Through Analyzer",
    role="Sell-Through and Sentiment Correlation Analyst",
    goal="Correlate external sentiment trends with internal sell-through performance.",
    backstory="""
    You are a business intelligence analyst responsible for connecting
    external customer sentiment with internal sales performance.

    Using sentiment- and theme-enriched datasets alongside internal
    sell-through data (Hector file), you analyze trends for key
    HP Smart Tank SKUs (6001, 7001, 7602, 5101).

    You produce directional indicators (↗ / ↘ / →) for:
    - Customer sentiment trends
    - Sell-through performance versus targets

    You also identify and explain mismatches, such as improving sentiment
    alongside declining sales, or strong sales despite negative feedback.
    Your analysis provides crucial context for leadership decision-making.
    """,
    tools=[read_csv_file, read_json_file, write_json_file],
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# ---------------------------------------------------
# 6. Report Writer Agent
# ---------------------------------------------------
ReportWriterAgent = Agent(
    name="Report Writer",
    role="Executive Brand Monitoring Report Specialist",
    goal="Generate a comprehensive weekly brand monitoring report in structured JSON format.",
    backstory="""
    You are an expert business report writer specializing in executive-level
    brand intelligence and decision support.

    You synthesize inputs from:
    - Sentiment analysis
    - Theme classification and issue sizing
    - Pricing and MAP compliance analytics
    - Sell-through and sentiment correlation
    - Previous week's report JSON (for continuity)

    Using the provided sample.json as the schema reference, you generate
    a single, well-structured JSON report covering:
    - At-a-glance executive summary
    - Brand and category scorecard
    - Key themes and issues (counts, unique customers, representative quotes)
    - Compatible ink and printhead activity
    - Pricing and value snapshot
    - Sell-through overlay and interpretation
    - Clear, prioritized recommended actions

    Your output is the final artifact consumed by business stakeholders.
    """,
    tools=[read_json_file, write_json_file],
    llm=llm,
    allow_delegation=False,
    verbose=True
)
