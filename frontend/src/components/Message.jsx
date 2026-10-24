export default function Message({ role, text }) {
  const isUser = role === "user";

  return (
    <div
      className={isUser ? "message message-user" : "message message-bot"}
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        margin: "8px 0",
      }}
    >
      <div
        style={{
          maxWidth: "75%",
          padding: "10px 14px",
          borderRadius: "12px",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
          background: isUser ? "#2563eb" : "#f1f5f9",
          color: isUser ? "#ffffff" : "#0f172a",
        }}
      >
        <strong style={{ display: "block", fontSize: "0.8rem", marginBottom: 4 }}>
          {isUser ? "You" : "Bot"}
        </strong>
        <span>{text}</span>
      </div>
    </div>
  );
}
