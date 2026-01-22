from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import pandas as pd
import json
import os

class IssueSizingInput(BaseModel):
    reviews_csv: str = Field(..., description="Path to reviews_updated.csv")
    social_csv: str = Field(..., description="Path to social_posts_updated.csv")
    output_json: str = Field(..., description="Path to output issue_sizing.json")

class RunIssueSizingTool(BaseTool):
    name: str = "run_issue_sizing"
    description: str = (
        "Compute issue sizing metrics using pandas and write results to JSON. "
        "Handles reading CSVs, aggregations, and file output."
    )
    args_schema: Type[BaseModel] = IssueSizingInput

    def _run(self, reviews_csv: str, social_csv: str, output_json: str) -> str:
        try:
            # ----------------------------
            # Load data
            # ----------------------------
            reviews_df = pd.read_csv(reviews_csv)
            social_df = pd.read_csv(social_csv)

            combined = pd.concat([reviews_df, social_df], ignore_index=True)

            if "key_theme" not in combined.columns:
                return "Error: 'key_theme' column not found in input CSVs."

            # Drop missing themes
            combined = combined.dropna(subset=["key_theme"])

            # Determine customer identifier
            identifier_col = None
            for col in ["reviewUrl", "post_id", "premalink"]:
                if col in combined.columns:
                    identifier_col = col
                    break

            # ----------------------------
            # Compute metrics
            # ----------------------------
            results = []

            for theme, group in combined.groupby("key_theme"):
                total_mentions = len(group)

                if identifier_col:
                    unique_customers = group[identifier_col].nunique()
                else:
                    unique_customers = total_mentions  # fallback

                results.append({
                    "key_theme": theme,
                    "total_mentions": int(total_mentions),
                    "unique_customers": int(unique_customers),
                    "spike_detected": False  # placeholder (future enhancement)
                })

            output = {
                "issue_sizing": results
            }

            # ----------------------------
            # Write output
            # ----------------------------
            os.makedirs(os.path.dirname(output_json), exist_ok=True)

            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)

            return f"Issue sizing completed successfully. Output written to {output_json}"

        except Exception as e:
            return f"Issue sizing failed: {str(e)}"


run_issue_sizing = RunIssueSizingTool()
