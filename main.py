import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from quiz_data import quiz_data
import time

FONT_SIZE_LARGE = ("Helvetica", 20)
FONT_SIZE_MEDIUM = ("Helvetica", 16)
PADDING = 10
TIME_LIMIT = 60

root = tk.Tk()
root.title("Quiz App")
root.geometry("600x600")

# img = tk.PhotoImage(file="bg.png")
# l1 = tk.Label(root, image=img)
# l1.pack()

style = Style(theme="flatly")
style.configure("TLabel", font=FONT_SIZE_LARGE)
style.configure("TButton", font=FONT_SIZE_MEDIUM)

qs_label = ttk.Label(root, anchor="center", wraplength=500, padding=PADDING)
qs_label.pack(pady=PADDING)

choice_btns = []
for i in range(4):
    button = ttk.Button(root)
    button.pack(pady=5)
    choice_btns.append(button)

feedback_label = ttk.Label(root, anchor="center", padding=PADDING)
feedback_label.pack(pady=PADDING)

score = 0
score_label = ttk.Label(root, text="Score: 0/{}".format(len(quiz_data)), anchor="center", padding=PADDING)
score_label.pack(pady=PADDING)

timer_label = ttk.Label(root, text="", anchor="center", padding=PADDING)
timer_label.pack(pady=PADDING)

next_btn = ttk.Button(root, text="Next", state="disabled")
next_btn.pack(pady=PADDING)

start_again_btn = ttk.Button(root, text="Start Again")
start_again_btn.pack_forget()

current_question = 0
time_start = 0
time_taken = 0
timer = None


def show_developer_info():
    messagebox.showinfo("Developer Info", "This quiz app was developed by Haris.")


menubar = tk.Menu(root)
root.config(menu=menubar)

developer_menu = tk.Menu(menubar, tearoff=0)
developer_menu.add_command(label="Developer Info", command=show_developer_info)

menubar.add_cascade(label="Developer", menu=developer_menu)


def show_question():
    global time_start
    question = quiz_data[current_question]
    qs_label.config(text=question["question"])

    choices = question["choices"]
    for i in range(4):
        if i < len(choices):
            choice_btns[i].config(text=choices[i], state="normal")
        else:
            choice_btns[i].config(text="", state="disabled")

    feedback_label.config(text="")
    next_btn.config(state="disabled")

    # Start the timer if it's the first question
    if current_question == 0:
        time_start = time.time()
        update_timer()


def check_answer(choice):
    global score
    question = quiz_data[current_question]
    selected_choice = choice_btns[choice].cget("text")

    if selected_choice == question["answer"]:
        feedback_label.config(text="Correct!", foreground="green")
        score += 1
    else:
        feedback_label.config(text="Incorrect!", foreground="red")

    score_label.config(text="Score: {}/{}".format(score, len(quiz_data)))

    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")


def next_question():
    global current_question
    current_question += 1

    if current_question < len(quiz_data):
        show_question()
    else:
        end_quiz()


def restart_quiz():
    global current_question, score, time_start, time_taken
    current_question = 0
    score = 0
    score_label.config(text="Score: 0/{}".format(len(quiz_data)))
    start_again_btn.pack_forget()
    for button in choice_btns:
        button.pack(pady=5)
    next_btn.pack(pady=PADDING)
    time_start = 0
    time_taken = 0
    show_question()


def end_quiz():
    global time_taken
    time_taken = time.time() - time_start
    messagebox.showinfo("Quiz Completed",
                        "Quiz Completed! Final score: {}/{}\nTime taken: {:.2f} seconds".format(score, len(quiz_data),
                                                                                                time_taken))
    timer_label.config(text="Time taken: {:.2f} seconds".format(time_taken))
    start_again_btn.pack(pady=PADDING)
    for button in choice_btns:
        button.pack_forget()
    next_btn.pack_forget()


def update_timer():
    global timer
    time_elapsed = int(time.time() - time_start)
    time_left = max(TIME_LIMIT - time_elapsed, 0)
    timer_label.config(text="Time left: {}s".format(time_left))

    if time_left > 0:
        timer = root.after(1000, update_timer)
    else:
        end_quiz()


for i in range(4):
    choice_btns[i]["command"] = lambda i=i: check_answer(i)

next_btn["command"] = next_question
start_again_btn["command"] = restart_quiz

show_question()

root.mainloop()
