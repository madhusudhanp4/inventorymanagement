import { useState } from "react";
import { askRagQuestion } from "../services/ragService";

function RAGChat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoading(true);

    try {
      const response = await askRagQuestion(question);
      setAnswer(response.answer);
    } catch (error) {
      console.error(error);
      setAnswer("Failed to get response");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Inventory Assistant</h2>

      <textarea
        rows="4"
        cols="60"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question..."
      />

      <br />
      <br />

      <button onClick={handleAsk}>
        Ask
      </button>

      <br />
      <br />

      {loading && <p>Loading...</p>}

      {answer && (
        <div>
          <h3>Answer</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default RAGChat;