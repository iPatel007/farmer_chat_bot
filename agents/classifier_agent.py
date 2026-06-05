from prompts.prompts import CLASSIFIER_PROMPT
from service.llm_service import llm


def classify_query(question: str) -> str:
    """
    Classify whether the user query is related to
    farming/agriculture domain or not.

    Returns:
        FARM
        NOT_FARM
    """

    prompt = f"""
{CLASSIFIER_PROMPT}

USER QUESTION:
{question}

FINAL OUTPUT:
"""

    try:

        response = llm.invoke(prompt)

        result = response.content.strip().upper()

        # SAFETY NORMALIZATION
        if result == "FARM":
            return "FARM"

        if result == "NOT_FARM":
            return "NOT_FARM"

        # FALLBACK SAFETY
        if "FARM" in result:
            return "FARM"

        return "NOT_FARM"

    except Exception as e:

        print(f"Classifier Error: {e}")

        # SAFE DEFAULT
        return "NOT_FARM"