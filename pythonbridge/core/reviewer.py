from pythonbridge.core.config import load_environment
from pythonbridge.gh.client import get_diff, post_review
from pythonbridge.llm.groq import GroqLLM


def review_pr(payload: dict) -> list[dict]:
    load_environment()

    files = get_diff(payload)
    llm = GroqLLM()

    reviews = []
    for file in files:
        review = llm.review_code(file.patch) if file.patch else None
        reviews.append(
            {
                "filename": file.filename,
                "status": file.status,
                "review": review,
            }
        )

    post_review(payload, reviews)

    return reviews


if __name__ == "__main__":
    test_payload = {
        "number": 1,
        "repository": {"full_name": "owner/repo"},
        "installation": {"id": "12345"},
    }
    results = review_pr(test_payload)
    for r in results:
        print(r["review"])
