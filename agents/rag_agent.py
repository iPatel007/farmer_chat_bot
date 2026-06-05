from service.vector_service import get_vectorstore


vectorstore = get_vectorstore()


def retrieve_context(question: str):
    docs = vectorstore.similarity_search(question, k=3)

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])

    return context