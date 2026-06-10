import os
from dotenv import load_dotenv
from groq import Groq
import gradio as gr

from vector_store import retrieve

load_dotenv()

MODEL_NAME = "llama-3.3-70b-versatile"


def format_context(chunks):
    parts = []
    for i, chunk in enumerate(chunks, start=1):
        parts.append(
            f"[Source {i}: {chunk['source']} | chunk {chunk['chunk_index']}]\n"
            f"{chunk['text']}"
        )
    return "\n\n---\n\n".join(parts)


def generate_answer(question, chunks):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Missing GROQ_API_KEY. Add it to your .env file."

    client = Groq(api_key=api_key)
    context = format_context(chunks)

    system_prompt = """
You are a grounded RAG assistant for an unofficial CU Boulder student guide.
Answer using only the retrieved context.
Do not use outside knowledge.
Do not guess.
If the answer is not in the retrieved context, say:
"I do not have enough information in the provided documents to answer that."
Cite the source filename(s) used in your answer.
"""

    user_prompt = f"""
Retrieved context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def ask(question):
    if not question.strip():
        return "Please enter a question.", ""

    chunks = [
        chunk
        for chunk in retrieve(question, top_k=5)
        if chunk["distance"] < 0.75
    ]
    answer = generate_answer(question, chunks)

    sources = "\n".join(
        f"- {c['source']} | chunk {c['chunk_index']} | distance {c['distance']:.4f}"
        for c in chunks
    )

    return answer, sources


with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide to Surviving CU Boulder")
    gr.Markdown("Ask a question about CU Boulder student life.")

    question = gr.Textbox(label="Your question")
    button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Retrieved from", lines=8)

    button.click(ask, inputs=question, outputs=[answer, sources])
    question.submit(ask, inputs=question, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()