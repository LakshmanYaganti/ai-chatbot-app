import { useState } from "react";
import axios from "axios";
import ChatBox from "../components/Chatbox";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function ChatPage() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");

  const uploadDocument = async () => {
    if (!file || uploading) return;

    setUploading(true);
    setUploadStatus("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`${API_BASE_URL}/upload/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploadStatus(res.data.message || "Document processed successfully.");
      setFile(null);
    } catch (err) {
      setUploadStatus(
        err.response?.data?.detail ||
          "Upload failed. Only PDF and .txt files are supported."
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h1>AI Knowledge Chatbot</h1>
      <p>Upload a PDF or text document, then ask questions about it.</p>

      <section aria-label="Upload a document">
        <h2>Add a document</h2>
        <input
          type="file"
          accept=".pdf,.txt"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button onClick={uploadDocument} disabled={!file || uploading}>
          {uploading ? "Uploading…" : "Upload"}
        </button>
        {uploadStatus && <p>{uploadStatus}</p>}
      </section>

      <ChatBox />
    </div>
  );
}
