import tkinter as tk
from tkinter import scrolledtext
import requests
from threading import Thread

BACKEND_URL = "http://127.0.0.1:8000/chat"

# 🎨 Tron Theme Colors
BG_COLOR = "#0a0f1c"
USER_BUBBLE = "#00f5d4"   # neon cyan
BOT_BUBBLE = "#1f3b73"    # dark blue
TEXT_COLOR = "#ffffff"

class ChatWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚡ AI Assistant")
        self.root.geometry("420x550")
        self.root.configure(bg=BG_COLOR)

        # Chat display
        self.chat_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.chat_frame, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.chat_frame, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Input area
        input_frame = tk.Frame(self.root, bg=BG_COLOR)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.user_input = tk.Entry(
            input_frame,
            bg="#111827",
            fg="white",
            insertbackground="white"
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", lambda e: self.send_message())

        send_btn = tk.Button(
            input_frame,
            text="➤",
            bg="#00f5d4",
            fg="black",
            command=self.send_message
        )
        send_btn.pack(side=tk.RIGHT)

    def add_message(self, message, is_user=False):
        frame = tk.Frame(self.scrollable_frame, bg=BG_COLOR)

        bubble = tk.Label(
            frame,
            text=message,
            bg=USER_BUBBLE if is_user else BOT_BUBBLE,
            fg="black" if is_user else "white",
            wraplength=250,
            justify="left",
            padx=10,
            pady=5
        )

        if is_user:
            bubble.pack(anchor="e", padx=10, pady=5)
        else:
            bubble.pack(anchor="w", padx=10, pady=5)

        frame.pack(fill=tk.BOTH, expand=True)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def send_message(self):
        msg = self.user_input.get().strip()
        if not msg:
            return

        self.add_message(msg, is_user=True)
        self.user_input.delete(0, tk.END)

        # Typing indicator
        self.add_message("Typing...", is_user=False)

        Thread(target=self.get_response, args=(msg,)).start()

    def get_response(self, msg):
        try:
            response = requests.post(BACKEND_URL, json={"message": msg})
            reply = response.json().get("response", "No response")
        except Exception as e:
            reply = f"Error: {e}"

        # Remove "Typing..." and add real response
        self.scrollable_frame.after(0, lambda: self.update_bot_reply(reply))

    def update_bot_reply(self, reply):
        # Remove last widget (Typing...)
        for widget in self.scrollable_frame.winfo_children()[-1:]:
            widget.destroy()

        self.add_message(reply, is_user=False)

def main():
    app = ChatWindow()
    app.root.mainloop()

if __name__ == "__main__":
    main()