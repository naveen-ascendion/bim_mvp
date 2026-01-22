from fastapi import FastAPI
from utils.normalize_csv import normalize_if_needed
from my_crew.crew_runner import run_crew, save_report

app = FastAPI(title="Crew Runner API", description="API to run the crew and generate reports")

@app.post("/run-crew")
async def run_crew_endpoint():
    """
    Endpoint to run the crew and generate a report.
    Returns the report data and saves it to a file.
    """
    try:
        normalize_if_needed("data/19-01-2026/raw_reviews.csv", "data/19-01-2026/reviews.csv")
        normalize_if_needed("data/19-01-2026/raw_social_posts.csv", "data/19-01-2026/social_posts.csv")

        report_data = run_crew()
        filepath = save_report(report_data)
        return {
            "status": "success",
            "report_data": report_data,
            "saved_at": filepath
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)