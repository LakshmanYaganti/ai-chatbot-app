import { useEffect, useRef, useState } from "react";
import axios from "axios";
import Message from "./Message";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function ChatBox() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat, loading]);

  const sendMessage = async () => {
    const text = message.trim();
    if (!text || loading) return;

    setError("");
    setLoading(true);
    setChat((prev) => [...prev, { role: "user", text }]);
    setMessage("");

    try {
      const res = await axios.post(`${API_BASE_URL}/chat/`, { message: text });
      setChat((prev) => [...prev, { role: "bot", text: res.data.response }]);
    } catch (err) {
      const detail =
        err.response?.data?.detail ||
        "Could not reach the chatbot backend. Is it running on port 8000?";
      setError(detail);
      setChat((prev) => [
        ...prev,
        { role: "bot", text: "Sorry — something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div>
      <div>
        {chat.map((entry, i) => (
          <Message key={i} role={entry.role} text={entry.text} />
        ))}
        {loading && <Message role="bot" text="Thinking…" />}
        <div ref={bottomRef} />
      </div>

      {error && (
        <p role="alert" style={{ color: "#b91c1c" }}>
          {error}
        </p>
      )}

      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your documents…"
          disabled={loading}
          style={{ flex: 1 }}
        />
        <button onClick={sendMessage} disabled={loading || !message.trim()}>
          {loading ? "Sending…" : "Send"}
        </button>
      </div>
    </div>
  );
}
