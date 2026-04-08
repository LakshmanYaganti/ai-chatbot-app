import { useState } from "react";
import axios from "axios";

export default function ChatBox() {

  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {

    const res = await axios.post("http://localhost:8000/chat/", {
      message: message
    });

    setChat([...chat, { user: message, bot: res.data.response }]);
    setMessage("");
  };

  return (
    <div>

      {chat.map((c, i) => (
        <div key={i}>
          <p><b>You:</b> {c.user}</p>
          <p><b>Bot:</b> {c.bot}</p>
        </div>
      ))}

      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <button onClick={sendMessage}>Send</button>

    </div>
  );
}