import axios from "axios";

const API_URL = "http://localhost:8000/api/rag";

export const askRagQuestion = async (question) => {
  const response = await axios.post(`${API_URL}/ask`, {
    question,
  });

  return response.data;
};