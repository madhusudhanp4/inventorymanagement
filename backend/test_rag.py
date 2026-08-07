from rag.rag_service import ask_question

print("Starting...")

answer = ask_question(
    "What is the weather forecast for Mumbai?"
)

print("Answer:")
print(answer)

print("Done")