import tkinter as tk
from tkinter import scrolledtext
from groq import Groq
import time
import threading

class GroqChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quantum")
        self.master.configure(bg="#007bff") 

# go to groq playground website (https://console.groq.com/keys) and make a free API KEY copy it and paste below where ask


        self.client = Groq(api_key="YOUR_API_KEY_HERE")
        self.chat_history = tk.Text(master, width=60, height=20, bg="black", fg="white")
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    


        self.padding_label = tk.Label(master, text="", bg="#007bff")
        self.padding_label.grid(row=1, column=0)
        
       
        self.placeholder_label = tk.Label(master, text="Enter your message", fg="black", bg="#007bff")


        self.placeholder_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.query_box = scrolledtext.ScrolledText(master, width=60, height=4, wrap="word")
        self.query_box.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
 
        self.query_box.bind("<Return>", self.send_message)
        self.send_button = tk.Button(master, text="Send", command=self.send_message, bg="#007bff", fg="white")  # Blue color
        self.send_button.grid(row=3, column=1, padx=10, pady=5, sticky="e")
        


        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        


        

    def send_message(self, event=None):
        prompt = self.query_box.get("1.0", tk.END).strip()  
        if prompt.lower() == "quit now":
            self.master.destroy()
        elif prompt:
           
            threading.Thread(target=self.get_response_and_update_history, args=(prompt,), daemon=True).start()
            self.query_box.delete("1.0", tk.END)
            
        self.starttime = time.time()  

    def get_response_and_update_history(self, prompt):
        response = self.get_response(prompt)
        self.update_chat_history(prompt, response)
    
    def get_response(self, prompt):
        a = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=2,
            max_tokens=4096,
            top_p=1,
            stream=True,
            stop=None
        )
        response = ""
        for chunk in a:
            response += chunk.choices[0].delta.content or ""
        return response
    
    def update_chat_history(self, prompt, response):
        self.chat_history.insert(tk.END, f"User: {prompt}\n", "user")
        self.chat_history.insert(tk.END, f"Quantum: {response}\n\n", "bot")
        endtime = time.time()
        elapsed_time = endtime - self.starttime








    
        self.chat_history.insert(tk.END, f"TIME TAKEN: {elapsed_time:.2f} seconds\n\n", "time")
        self.chat_history.see(tk.END)

def main():
    root = tk.Tk()
    app = GroqChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
