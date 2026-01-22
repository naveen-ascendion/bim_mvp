from crewai import Task
from my_crew.my_agents import (
    SentimentAgent,
    ThemeClassifierAgent,
    PricingAgent,
    IssueSizingAgent,
    SellThroughAgent,
    ReportWriterAgent
)

DATE = "19-01-2026"
DATA_DIR = f"data/{DATE}"
ANALYTICS_DIR = f"analytics/{DATE}"

# ===================================================
# 1. SENTIMENT ANALYSIS TASK
# ===================================================
sentiment_task = Task(
    description=f"""
You MUST follow these exact steps. Do NOT skip steps.

STEP 1:
Use read_csv_file to read:
- {DATA_DIR}/reviews.csv

STEP 2:
For EACH row, infer sentiment using:
- reviewTitle
- reviewDescription
- ratingScore

Allowed sentiment values:
- positive
- negative
- neutral

STEP 3:
Create a Python list named sentiment_values
(one value per row, same order).

STEP 4:
Call write_csv_with_column with:
- input_csv_path = "{DATA_DIR}/reviews.csv"
- output_csv_path = "{ANALYTICS_DIR}/reviews_updated.csv"
- column_name = "sentiment"
- column_values = sentiment_values

STEP 5:
Repeat STEPS 1–4 for:
- input_csv_path = "{DATA_DIR}/social_posts.csv"
- output_csv_path = "{ANALYTICS_DIR}/social_posts_updated.csv"

You MUST call write_csv_with_column.
Do NOT return free text.
""",
    agent=SentimentAgent,
    expected_output=f"""
CSV files created:
- {ANALYTICS_DIR}/reviews_updated.csv
- {ANALYTICS_DIR}/social_posts_updated.csv
"""
)

# ===================================================
# 2. THEME CLASSIFICATION TASK (IN-PLACE UPDATE)
# ===================================================
theme_classification_task = Task(
    description=f"""
You MUST follow these exact steps.

STEP 1:
Use read_csv_file to read:
- {ANALYTICS_DIR}/reviews_updated.csv

STEP 2:
For EACH row, infer ONE key theme from review text.
Allowed themes include (but are not limited to):
- printhead_failure
- ink_leakage
- setup_or_wifi_issue
- ink_clogging_or_drying
- compatible_ink_usage
- reliability_issue
- performance_or_speed
- general_feedback

STEP 3:
Create a Python list named key_theme_values.

STEP 4:
Call write_csv_with_column with:
- input_csv_path = "{ANALYTICS_DIR}/reviews_updated.csv"
- output_csv_path = "{ANALYTICS_DIR}/reviews_updated.csv"
- column_name = "key_theme"
- column_values = key_theme_values

STEP 5:
Repeat STEPS 1–4 for:
- {ANALYTICS_DIR}/social_posts_updated.csv

You MUST call write_csv_with_column.
Do NOT return free text.
""",
    agent=ThemeClassifierAgent,
    expected_output=f"""
CSV files updated in-place:
- {ANALYTICS_DIR}/reviews_updated.csv
- {ANALYTICS_DIR}/social_posts_updated.csv
"""
)

# ===================================================
# 3. ISSUE SIZING TASK
# ===================================================
issue_sizing_task = Task(
    description=f"""
You MUST follow these exact steps.

STEP 1:
Use read_csv_file to read:
- {ANALYTICS_DIR}/reviews_updated.csv
- {ANALYTICS_DIR}/social_posts_updated.csv

STEP 2:
Compute issue sizing metrics per key_theme:
- total_mentions
- unique_customers (use reviewUrl or post identifier)
- detect theme spikes if any

STEP 3:
Construct a single JSON object with this structure:
{{
  "issue_sizing": [
    {{
      "key_theme": "...",
      "total_mentions": <int>,
      "unique_customers": <int>,
      "spike_detected": <true|false>
    }}
  ]
}}

STEP 4:
Call write_json_file with:
- output_path = "{ANALYTICS_DIR}/issue_sizing.json"
- json_data = constructed_object

You MUST call write_json_file.
Do NOT return free text.
""",
    agent=IssueSizingAgent,
    expected_output=f"""
JSON file created:
- {ANALYTICS_DIR}/issue_sizing.json
"""
)

# ===================================================
# 4. PRICING ANALYSIS TASK
# ===================================================
pricing_analysis_task = Task(
    description=f"""
You MUST follow these exact steps.

STEP 1:
Use read_csv_file to read pricing inputs
(if products.csv exists).

STEP 2:
Compute pricing metrics:
- street_price_index
- promo_discount_intensity
- bottle_cpp
- map_violations (HP $17.99 / $18.99)

STEP 3:
Construct a JSON object with clear metric keys.

STEP 4:
Call write_json_file with:
- output_path = "{ANALYTICS_DIR}/pricing_analysis.json"
- json_data = constructed_object

You MUST call write_json_file.
Do NOT return free text.
""",
    agent=PricingAgent,
    expected_output=f"""
JSON file created:
- {ANALYTICS_DIR}/pricing_analysis.json
"""
)

# ===================================================
# 5. SELL-THROUGH ANALYSIS TASK
# ===================================================
sell_through_task = Task(
    description=f"""
You MUST follow these exact steps.

STEP 1:
Use read_csv_file to read:
- {ANALYTICS_DIR}/reviews_updated.csv
- {ANALYTICS_DIR}/social_posts_updated.csv
- {DATA_DIR}/hector.csv

STEP 2:
Aggregate sentiment trends for HP Smart Tank SKUs:
6001, 7001, 7602, 5101.

STEP 3:
Compare sentiment trends with sell-through data.

STEP 4:
Assign directional indicators:
- ↗ increasing
- ↘ decreasing
- → flat

STEP 5:
Construct a JSON object with:
- sku
- sentiment_trend
- sell_through_trend
- mismatch_commentary

STEP 6:
Call write_json_file with:
- output_path = "{ANALYTICS_DIR}/sell_through_analysis.json"
- json_data = constructed_object

You MUST call write_json_file.
Do NOT return free text.
""",
    agent=SellThroughAgent,
    expected_output=f"""
JSON file created:
- {ANALYTICS_DIR}/sell_through_analysis.json
"""
)

# ===================================================
# 6. FINAL REPORT WRITER TASK (CRITICAL)
# ===================================================
report_writer_task = Task(
    description=f"""
You MUST follow these exact steps.

STEP 1:
Use read_json_file to read:
- {ANALYTICS_DIR}/issue_sizing.json
- {ANALYTICS_DIR}/pricing_analysis.json
- {ANALYTICS_DIR}/sell_through_analysis.json
- sample.json (schema reference)

STEP 2:
Merge all inputs into ONE JSON object that
STRICTLY matches the structure of sample.json.

STEP 3:
Ensure all required sections exist:
- At-a-glance summary
- Scorecard
- Themes & Issues
- Pricing & Value
- Sell-through overlay
- Recommended actions

STEP 4:
Call write_json_file with:
- output_path = "weekly_reports/{DATE}.json"
- json_data = final_object

You MUST call write_json_file.
Do NOT return free text.
""",
    agent=ReportWriterAgent,
    expected_output=f"""
Final report JSON created:
- final_report_{DATE}.json
"""
)
