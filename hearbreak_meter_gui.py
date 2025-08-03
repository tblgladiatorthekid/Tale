import tkinter as tk
from tkinter import messagebox
from collections import defaultdict

class HeartbreakMeter:
    def __init__(self):
        self.heartbreak_counter = 0
        self.heartbreaks = []  # Each entry is a dict: {'person': ..., 'reason': ..., 'rating': ...}
        self.max_limit = 100

    def add_heartbreak(self, person, reason, rating):
        if self.heartbreak_counter + rating > self.max_limit:
            return False, self.heartbreak_counter
        self.heartbreaks.append({"person": person, "reason": reason, "rating": rating})
        self.heartbreak_counter += rating
        return True, self.heartbreak_counter

    def get_leaderboard(self):
        scores = defaultdict(int)
        for h in self.heartbreaks:
            scores[h["person"]] += h["rating"]
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

class HeartbreakApp:
    def __init__(self, root):
        self.meter = HeartbreakMeter()
        self.root = root
        self.root.title("💔 Heartbreak Meter 💔")
        self.root.configure(bg="#f2e6e9")

        # Font
        self.custom_font = ("Segoe Script", 11, "italic")

        # Input: Person
        tk.Label(root, text="Who broke your heart?", font=self.custom_font, bg="#f2e6e9").pack(pady=(15, 5))
        self.person_entry = tk.Entry(root, font=self.custom_font, width=40)
        self.person_entry.pack()

        # Input: Reason
        tk.Label(root, text="But why?", font=self.custom_font, bg="#f2e6e9").pack(pady=(10, 5))
        self.reason_entry = tk.Entry(root, font=self.custom_font, width=40)
        self.reason_entry.pack()

        # Input: Rating
        tk.Label(root, text="How painful was it? (0–100):", font=self.custom_font, bg="#f2e6e9").pack(pady=(10, 5))
        self.rating_entry = tk.Entry(root, font=self.custom_font, width=40)
        self.rating_entry.pack()

        # Submit Button
        tk.Button(root, text="Record Tragedy", command=self.submit_heartbreak,
                  bg="#d6a4a4", font=self.custom_font).pack(pady=12)

        # Leaderboard Button
        tk.Button(root, text="Show Leaderboard", command=self.show_leaderboard,
                  bg="#c4b5b5", font=self.custom_font).pack(pady=4)

        # Message
        self.message = tk.Label(root, text="", font=self.custom_font, fg="red", bg="#f2e6e9")
        self.message.pack(pady=15)

    def submit_heartbreak(self):
        person = self.person_entry.get().strip()
        reason = self.reason_entry.get().strip()
        try:
            rating = int(self.rating_entry.get())
        except ValueError:
            self.message.config(text="Please enter a valid number.")
            return

        if not person or rating < 0 or rating > 100:
            self.message.config(text="Enter a name and a rating between 0 and 100.")
            return

        success, counter = self.meter.add_heartbreak(person, reason, rating)
        if not success:
            self.message.config(text=(
                "💔 I'm so sorry. You deserve to be loved.\n"
                "But I'm telling you, you are loved.\n"
                "Even if you feel you're alone, don't let your light go out.\n"
                "You're still here, and you're brave for doing that."
            ))
        else:
            self.message.config(text=f"Heartbreak recorded. Current heartbreak level: {counter}/100")

        # Clear entries
        self.person_entry.delete(0, tk.END)
        self.reason_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def show_leaderboard(self):
        board = self.meter.get_leaderboard()
        if not board:
            messagebox.showinfo("Leaderboard", "No heartbreaks yet.")
            return
        result = "\n".join(f"{p}: {r}" for p, r in board)
        messagebox.showinfo("Leaderboard", f"💔 Heartbreak Leaderboard 💔\n\n{result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HeartbreakApp(root)
    root.mainloop()
