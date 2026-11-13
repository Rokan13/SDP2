import tkinter as tk
from tkinter import messagebox

# databasecode.py থেকে ব্যাকএন্ড ফাংশনগুলো ইমপোর্ট করছি
try:
    from databasecode import (
        get_all_cases, 
        get_all_suspects, 
        get_all_statements, 
        get_all_evidence, 
        get_solution
    )
except ImportError:
    pass

# মেইন উইন্ডো তৈরি
root = tk.Tk()
root.title("Crime Tracking & Forensics System")
root.geometry("800x680")

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# --- Step 1: Welcome Screen ---
def show_welcome_screen():
    clear_screen()
    
    title_label = tk.Label(root, text="Crime Investigation System", font=("Arial", 18, "bold"), fg="darkblue")
    title_label.pack(pady=30)
    
    desc_label = tk.Label(root, text="Project Name: Crime Tracking & Forensics System\nWelcome investigator! Choose an option below to proceed.", font=("Arial", 11), justify="center")
    desc_label.pack(pady=15)

    # মূল অপশন বাটনগুলো
    start_btn = tk.Button(root, text="Start Investigation (All Cases)", font=("Arial", 11, "bold"), bg="navy", fg="white", width=30, pady=8, command=lambda: show_case_selection("All"))
    start_btn.pack(pady=8)

    solved_btn = tk.Button(root, text="View Solved Cases", font=("Arial", 11), bg="darkgreen", fg="white", width=30, pady=6, command=lambda: show_case_selection("Solved"))
    solved_btn.pack(pady=8)

    unsolved_btn = tk.Button(root, text="View Unsolved Cases", font=("Arial", 11), bg="darkorange", fg="white", width=30, pady=6, command=lambda: show_case_selection("Unsolved"))
    unsolved_btn.pack(pady=8)

    exit_btn = tk.Button(root, text="Exit Application", font=("Arial", 11), bg="red", fg="white", width=30, pady=6, command=root.destroy)
    exit_btn.pack(pady=15)

# --- Step 2 & 3: Case Selection Screen (Filter Wise) ---
def show_case_selection(filter_type="All"):
    clear_screen()

    title_text = "Select a Case to Investigate"
    if filter_type == "Solved":
        title_text = "Solved Cases Archive"
    elif filter_type == "Unsolved":
        title_text = "Unsolved Cases List"

    heading = tk.Label(root, text=title_text, font=("Arial", 14, "bold"))
    heading.pack(pady=15)

    try:
        cases = get_all_cases()
    except Exception:
        cases = []

    # ফিল্টার অনুযায়ী কেস আলাদা করা (ডেমো হিসেবে স্ট্যাটাস চেক করা)
    filtered_cases = []
    for c in cases:
        # c[6] হলো status ('Unsolved' বা 'Solved')
        status = c[6] if len(c) > 6 else 'Unsolved'
        if filter_type == "All":
            filtered_cases.append(c)
        elif filter_type == "Solved" and status == 'Solved':
            filtered_cases.append(c)
        elif filter_type == "Unsolved" and status == 'Unsolved':
            filtered_cases.append(c)

    if not filtered_cases:
        no_case_label = tk.Label(root, text=f"No {filter_type.lower()} cases found in database!", fg="red", font=("Arial", 11))
        no_case_label.pack(pady=20)
    else:
        for case in filtered_cases:
            case_id = case[0]
            case_title = case[1]
            case_type = case[2]
            status = case[6] if len(case) > 6 else 'Unsolved'
            
            btn_text = f"ID: {case_id} | {case_title} ({case_type}) - [{status}]"
            case_btn = tk.Button(root, text=btn_text, width=65, font=("Arial", 10), bg="lightgray", command=lambda cid=case_id, ctitle=case_title, ctype=case_type, cdesc=case[3], cloc=case[4], cdate=case[5]: open_case_details(cid, ctitle, ctype, cdesc, cloc, cdate))
            case_btn.pack(pady=5)

    # নেভিগেশন বাটন
    nav_frame = tk.Frame(root)
    nav_frame.pack(pady=20)

    tk.Button(nav_frame, text="Back to Home", font=("Arial", 10), bg="orange", width=20, command=show_welcome_screen).pack(side="left", padx=10)

# --- Step 4, 5, 6, 7 & 8: Case Details, Suspects, Evidence & Culprit Selection ---
def open_case_details(case_id, case_title, case_type, description, location, incident_date):
    clear_screen()

    # স্ক্রল করার জন্য ক্যানভাস ও ফ্রেম
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # কেসের তথ্য
    heading = tk.Label(scrollable_frame, text=f"Case: {case_title}", font=("Arial", 14, "bold"), fg="darkgreen")
    heading.pack(pady=10)

    info_text = f"Type: {case_type} | Location: {location} | Date: {incident_date}\nDescription: {description}"
    desc_label = tk.Label(scrollable_frame, text=info_text, font=("Arial", 10), justify="left", fg="black")
    desc_label.pack(pady=5)

    # সাসপেক্ট ও স্টেটমেন্ট লোড করা
    tk.Label(scrollable_frame, text="--- Suspects, Statements & Alibi ---", font=("Arial", 11, "bold"), fg="purple").pack(pady=5)

    try:
        suspects = get_all_suspects(case_id)
        statements = get_all_statements(case_id)
    except:
        suspects = []
        statements = []

    selected_suspect_var = tk.IntVar()

    if suspects:
        for s in suspects:
            s_id, s_case_id, s_name, s_age, s_occ, s_addr = s
            s_statement = "No statement."
            s_alibi = "N/A"
            for st in statements:
                if st[2] == s_id:
                    s_statement = st[3]
                    s_alibi = st[4]
            
            s_info = f"[{s_name}] (Age: {s_age}, Occ: {s_occ})\nStatement: {s_statement}\nAlibi: {s_alibi}"
            r_btn = tk.Radiobutton(scrollable_frame, text=s_info, variable=selected_suspect_var, value=s_id, font=("Arial", 9), justify="left", anchor="w")
            r_btn.pack(pady=3, fill="x", padx=40)
    else:
        tk.Label(scrollable_frame, text="No suspects found.", font=("Arial", 9)).pack()

    # এভিডেন্স লোড করা
    tk.Label(scrollable_frame, text="--- Evidence ---", font=("Arial", 11, "bold"), fg="brown").pack(pady=5)

    try:
        evidences = get_all_evidence(case_id)
    except:
        evidences = []

    if evidences:
        for e in evidences:
            e_name, e_type, e_desc = e[2], e[3], e[4]
            e_info = f"• {e_name} ({e_type}) - {e_desc}"
            tk.Label(scrollable_frame, text=e_info, font=("Arial", 9), fg="blue").pack(pady=2)
    else:
        tk.Label(scrollable_frame, text="No evidence collected.", font=("Arial", 9)).pack()

    # Reveal Button
    def reveal_solution():
        chosen_suspect_id = selected_suspect_var.get()
        if chosen_suspect_id == 0:
            messagebox.showwarning("Warning", "Please select a suspect as the culprit before clicking Reveal!")
            return
        
        solution = get_solution(case_id)
        if not solution:
            messagebox.showerror("Error", "Solution not found for this case!")
            return
        
        real_culprit_id = solution[2]
        real_culprit_name = solution[3]
        explanation = solution[4]

        show_result_screen(chosen_suspect_id == real_culprit_id, real_culprit_name, explanation, case_id)

    reveal_btn = tk.Button(scrollable_frame, text="Click Reveal (Check Culprit)", font=("Arial", 11, "bold"), bg="darkred", fg="white", padx=10, pady=5, command=reveal_solution)
    reveal_btn.pack(pady=15)

    back_to_cases = tk.Button(scrollable_frame, text="Back to Case List", font=("Arial", 10), bg="orange", command=lambda: show_case_selection("All"))
    back_to_cases.pack(pady=10)

# --- Step 9 & 10: Result Screen & New Options ---
def show_result_screen(is_correct, culprit_name, explanation, case_id):
    clear_screen()

    if is_correct:
        res_title = "Congratulations! Case Solved 🎉"
        res_color = "green"
    else:
        res_title = "Wrong Answer, Sorry! ❌"
        res_color = "red"

    tk.Label(root, text=res_title, font=("Arial", 16, "bold"), fg=res_color).pack(pady=20)
    
    if not is_correct:
        tk.Label(root, text=f"The actual culprit was: {culprit_name}", font=("Arial", 11, "bold")).pack(pady=5)

    exp_text = f"--- Case Explanation ---\n{explanation}"
    tk.Label(root, text=exp_text, font=("Arial", 10), wraplength=600, justify="center").pack(pady=15)

    tk.Label(root, text="What would you like to do next?", font=("Arial", 11, "bold")).pack(pady=10)

    # তোমার চাওয়া অপশনগুলো (Back home, Try another case, Solved/Unsolved view ইত্যাদি)
    tk.Button(root, text="Try Another Case", font=("Arial", 10), bg="lightblue", width=30, command=lambda: show_case_selection("All")).pack(pady=5)
    tk.Button(root, text="View Solved Cases", font=("Arial", 10), bg="lightgreen", width=30, command=lambda: show_case_selection("Solved")).pack(pady=5)
    tk.Button(root, text="View Unsolved Cases", font=("Arial", 10), bg="gold", width=30, command=lambda: show_case_selection("Unsolved")).pack(pady=5)
    tk.Button(root, text="Back to Home", font=("Arial", 10), bg="orange", width=30, command=show_welcome_screen).pack(pady=5)
    tk.Button(root, text="Exit Application", font=("Arial", 10), bg="red", fg="white", width=30, command=root.destroy).pack(pady=5)

# অ্যাপ রান করার জন্য ওয়েলকাম স্ক্রিন কল করা হলো
show_welcome_screen()

root.mainloop()