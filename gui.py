import tkinter as tk
from tkinter import messagebox

from database import (
    create_tables,
    get_all_suspects,
    get_all_statements,
    get_all_evidence
)
from case_management import (
    insert_cases,
    get_case_list,
    get_case_details,
    insert_all_case_solutions
)
from evidence import load_all_case_evidence
from solve_case import check_answer, get_solution_result


def initialize_database():
    create_tables()
    insert_cases()
    load_all_case_evidence()
    insert_all_case_solutions()


# ==========================================================
# ৫ নম্বর পেজ: View All Cases
# ==========================================================
def show_all_cases_page():
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(
        main_frame,
        text="CASE CLOSED - ALL CASES",
        font=("Arial", 16, "bold"),
        bg="#1e1e2e",
        fg="#cdd6f4"
    ).pack(pady=15)

    cases = get_case_list()

    if not cases:
        tk.Label(main_frame, text="No cases found in database.", bg="#1e1e2e", fg="white").pack()
        return

    for case in cases:
        case_id, title, c_type, _, _, _, status = case
        btn_text = f"#{case_id}  |  {title}   [{c_type}]   —   Status: {status}"

        tk.Button(
            main_frame,
            text=btn_text,
            font=("Arial", 11),
            bg="#313244",
            fg="white",
            activebackground="#45475a",
            activeforeground="white",
            anchor="w",
            padx=15,
            pady=8,
            command=lambda cid=case_id: show_case_details_page(cid)
        ).pack(fill="x", padx=30, pady=5)


# ==========================================================
# ৬ নম্বর পেজ: Case এ ঢুকার পর (Case Details)
# ==========================================================
def show_case_details_page(case_id):
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Top Navigation Bar (Back & Exit)
    nav_frame = tk.Frame(main_frame, bg="#1e1e2e")
    nav_frame.pack(fill="x", padx=20, pady=10)

    tk.Button(
        nav_frame, text="<- Back", bg="#f38ba8", fg="black",
        font=("Arial", 10, "bold"), command=show_all_cases_page
    ).pack(side="left")

    tk.Button(
        nav_frame, text="Exit", bg="#eba0ac", fg="black",
        font=("Arial", 10, "bold"), command=root.destroy
    ).pack(side="right")

    # Scrollable Canvas তৈরি
    canvas = tk.Canvas(main_frame, bg="#1e1e2e", highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    content_frame = tk.Frame(canvas, bg="#1e1e2e")

    content_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=20)
    scrollbar.pack(side="right", fill="y")

    # ১. Case Info লোড
    info = get_case_details(case_id)
    if info:
        tk.Label(
            content_frame,
            text=f"Case #{info['case_id']}: {info['case_title']} ({info['case_type']})",
            font=("Arial", 15, "bold"), bg="#1e1e2e", fg="#89b4fa"
        ).pack(anchor="w", pady=(5, 2))

        tk.Label(
            content_frame,
            text=f"Location: {info['location']}  |  Date: {info['incident_date']}  |  Status: {info['status']}",
            font=("Arial", 10, "italic"), bg="#1e1e2e", fg="#a6adc8"
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            content_frame,
            text=info["description"],
            font=("Arial", 11), bg="#1e1e2e", fg="white",
            wraplength=760, justify="left"
        ).pack(anchor="w", pady=(0, 12))

    # ২. Suspects লোড
    suspects = get_all_suspects(case_id)
    suspect_map = {}
    tk.Label(content_frame, text="SUSPECTS:", font=("Arial", 12, "bold"), bg="#1e1e2e", fg="#f9e2af").pack(anchor="w", pady=(8, 3))

    if not suspects:
        tk.Label(content_frame, text="No suspects loaded yet.", bg="#1e1e2e", fg="#a6adc8").pack(anchor="w")
    else:
        for s in suspects:
            s_id, _, s_name, age, occ, addr = s
            suspect_map[s_id] = s_name
            tk.Label(
                content_frame,
                text=f"• {s_name} (Age: {age}, {occ}) — Address: {addr}",
                font=("Arial", 10), bg="#1e1e2e", fg="white"
            ).pack(anchor="w", padx=10)

    # ৩. Statements লোড
    statements = get_all_statements(case_id)
    tk.Label(content_frame, text="STATEMENTS:", font=("Arial", 12, "bold"), bg="#1e1e2e", fg="#f9e2af").pack(anchor="w", pady=(12, 3))

    if not statements:
        tk.Label(content_frame, text="No statements loaded yet.", bg="#1e1e2e", fg="#a6adc8").pack(anchor="w")
    else:
        for st in statements:
            _, _, s_id, text, alibi, _ = st
            s_name = suspect_map.get(s_id, f"Suspect #{s_id}")
            tk.Label(
                content_frame,
                text=f"• {s_name}: \"{text}\"  [Alibi: {alibi}]",
                font=("Arial", 10), bg="#1e1e2e", fg="white",
                wraplength=750, justify="left"
            ).pack(anchor="w", padx=10, pady=2)

    # ৪. Evidence লোড
    evidences = get_all_evidence(case_id)
    tk.Label(content_frame, text="EVIDENCE:", font=("Arial", 12, "bold"), bg="#1e1e2e", fg="#f9e2af").pack(anchor="w", pady=(12, 3))

    for ev in evidences:
        _, _, ev_name, ev_type, ev_desc, _ = ev
        tk.Label(
            content_frame,
            text=f"• [{ev_type}] {ev_name}: {ev_desc}",
            font=("Arial", 10), bg="#1e1e2e", fg="white",
            wraplength=750, justify="left"
        ).pack(anchor="w", padx=10, pady=2)

    # ৫. Choose Suspect & Case Solution সেকশন
    tk.Label(content_frame, text="CHOOSE SUSPECT:", font=("Arial", 12, "bold"), bg="#1e1e2e", fg="#a6e3a1").pack(anchor="w", pady=(15, 5))

    selected_suspect = tk.IntVar(value=-1)
    for s in suspects:
        tk.Radiobutton(
            content_frame, text=s[2], variable=selected_suspect, value=s[0],
            font=("Arial", 11), bg="#1e1e2e", fg="white", selectcolor="#313244",
            activebackground="#1e1e2e", activeforeground="white"
        ).pack(anchor="w", padx=15)

    solution_label = tk.Label(
        content_frame, text="", font=("Arial", 11, "bold"),
        bg="#1e1e2e", fg="#a6e3a1", wraplength=750, justify="left"
    )
    solution_label.pack(anchor="w", pady=10)

    def handle_solve():
        chosen_id = selected_suspect.get()
        if chosen_id == -1:
            messagebox.showwarning("Warning", "Please select a suspect first!")
            return

        is_correct = check_answer(case_id, chosen_id)
        sol = get_solution_result(case_id)

        if sol is None:
            messagebox.showinfo("Info", "Solution not found in database (make sure suspects are inserted first).")
            return

        if is_correct:
            messagebox.showinfo("Case Solved!", f"Correct! {sol['culprit_name']} is the real culprit.")
        else:
            messagebox.showerror("Wrong Suspect", f"Incorrect! The real culprit was {sol['culprit_name']}.")

        solution_label.config(
            text=f"CASE SOLUTION:\nReal Culprit: {sol['culprit_name']}\nExplanation: {sol['explanation']}"
        )

    tk.Button(
        content_frame, text="Submit Suspect", font=("Arial", 11, "bold"),
        bg="#89b4fa", fg="black", padx=15, pady=5, command=handle_solve
    ).pack(anchor="w", pady=10)


# ==========================================================
# মেইন উইন্ডো চালু করা
# ==========================================================
if __name__ == "__main__":
    initialize_database()

    root = tk.Tk()
    root.title("Case Closed - Crime Tracking & Forensics System")
    root.geometry("850x620")
    root.configure(bg="#1e1e2e")

    main_frame = tk.Frame(root, bg="#1e1e2e")
    main_frame.pack(fill="both", expand=True)

    show_all_cases_page()
    root.mainloop()