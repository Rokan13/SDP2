from tkinter import *

root = Tk()
root.title("Case Closed_ Crime Tracking System")
root.geometry("500x500")
root.config(bg="#1e1e1e") # background colour balck

def show_welcome_screen():
    for widget in root.winfo_children():
        widget.destroy()

    label_title = Label(root,
                        text="Case Closed",
                        font=("Arial",22,"bold"),
                        fg="white",
                        bg="#1e1e1e")
    label_title.pack(pady=10)

    label_sub = Label(root,
                      text="Crime Tracking & Forensics System",
                      font=("Arial",12),
                      fg="#aaaaaa",
                      bg="#1e1e1e"
                      )           
    label_sub.pack(pady=10)

    btn_start = Button(
        root, 
        text="Start Investigation",  ##
        font=("Arial", 14, "bold"), 
        bg="#28a745", 
        fg="white", 
        padx=20, 
        pady=10, 
        command=show_menu_screen
    )
    btn_start.pack(pady=40)        

def show_menu_screen():
    for widget in root.winfo_children():
        widget.destroy()

    label_heading = Label(root,
                          text="Criminal Investigation System",
                          font=("Arial",16,"bold"),
                          bg="#1e1e1e"
                          )    
    label_heading.pack(pady=20)

    label_desc = Label(root,
                              text="Welcome investigator! Chose an Option below to proceed.",
                              font=("Arial",16,"bold"),
                              bg="#1e1e1e"
                              )    
    label_desc.pack(pady=5)


    btn_all_cases = Button(root, text="Show Cases)", width=35, font=("Arial", 11, "bold"), bg="#003366", fg="white", pady=5, command=show_case_selection)
    btn_all_cases.pack(pady=8)

    
    btn_solved = Button(root, text="View Solved Cases", width=35, font=("Arial", 11, "bold"), bg="#28a745", fg="white", pady=5, command=lambda: print("View Solved Clicked"))
    btn_solved.pack(pady=8)

    
    btn_unsolved = Button(root, text="View Unsolved Cases", width=35, font=("Arial", 11, "bold"), bg="#d97706", fg="white", pady=5, command=show_case_selection)
    btn_unsolved.pack(pady=8)

    
    btn_exit = Button(root, text="Exit Application", width=35, font=("Arial", 11, "bold"), bg="#dc3545", fg="white", pady=5, command=root.quit)
    btn_exit.pack(pady=8)

    btn_back = Button(
        root,
        text="Back to Home",
        font=("Arial", 9),
        bg="#555555",
        fg="white",
        command=show_menu_screen
    ) 
    btn_back.pack(pady=15)



def show_case_selection():
    for widget in root.winfo_children():
        widget.destroy()

    label_heading = Label(root,
                          text="Select an Unsolved Case",
                          font=("Arial", 16, "bold"),
                          fg="white",
                          bg="#1e1e1e"
                          )     
    label_heading.pack(pady=20)

    

    def on_case_selected(case_name):
        print(f"Selected : {case_name}")


    btn_case1 = Button(root, text="Case #001: The 11:47 PM Disappearance", width=40, font=("Arial", 10), command=lambda: on_case_selected("Case 001"))
    btn_case1.pack(pady=8)
    
    btn_case2 = Button(root, text="Case #002: The Last Message", width=40, font=("Arial", 10), command=lambda: on_case_selected("Case 002"))
    btn_case2.pack(pady=8)
    
    btn_case3 = Button(root, text="Case #003: The Vanishing Diamond", width=40, font=("Arial", 10), command=lambda: on_case_selected("Case 003"))
    btn_case3.pack(pady=8)

    btn_case4 = Button(root, text="Case #004: The Missing Prototype", width=40, font=("Arial", 10), command=lambda: on_case_selected("Case 004"))
    btn_case4.pack(pady=8)  

    btn_back = Button(
        root,
        text="Back to Home",
        font=("Arial", 10),
        bg="#dc3545",
        fg="white",
        command = show_menu_screen
    ) 

    btn_back.pack(pady=30)

show_welcome_screen()


root.mainloop()
