from prompts.prompts import ANSWER_PROMPT
from service.llm_service import llm


def generate_answer(question, context):
    prompt = ANSWER_PROMPT.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt)

    return response.content