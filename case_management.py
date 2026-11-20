
from database import (
    add_case,
    get_all_cases,
    get_all_suspects,
    add_solution,
    get_solution
)


#             ALL 10 CASES

CASES_DATA = [

    (
        "The 11:47 PM Disappearance",
        "Art Theft",
        "A rare diamond necklace valued at 5 crore disappeared from a secured glass display case during a private exhibition. The display case was not broken and the alarm system did not activate.",
        "Private Art Gallery, Dhaka",
        "15 October 2026"
    ),

    (
        "The Last Message",
        "Murder",
        "Dr. Rehan Karim was found dead in his study room. The door was locked from inside and there were no signs of forced entry. A laptop message delivered at 9:38 PM initially appeared to suggest he was alive at that time.",
        "Victim's apartment, Dhaka",
        "22 October 2026"
    ),

    (
        "The Vanishing Diamond",
        "Theft",
        "A valuable historical necklace known as The Queen's Diamond disappeared from a locked display case at the Royal Heritage Museum. The display case showed no visible damage and the alarm system did not report a break-in.",
        "Royal Heritage Museum, Dhaka",
        "5 November 2026"
    ),

    (
        "The Missing Prototype",
        "Theft",
        "A working prototype of a smart navigation device disappeared from a locked project room at Northbridge Technology Institute. The room showed no signs of forced entry.",
        "Project Room 204, Northbridge Technology Institute",
        "12 October 2026"
    ),

    (
        "The Missing Blueprint",
        "Theft",
        "A valuable architectural blueprint for the new Riverside Science Centre disappeared from a locked display case at the Northstar Design Exhibition. It was confirmed to be inside the case at 8:10 PM on 18 October 2026, but was missing when the case was checked at 8:35 PM. There were no signs of forced entry. The electronic access log later showed that the case had been opened with a temporary staff pass.",
        "Northstar Design Exhibition, Dhaka",
        "18 October 2026"
    ),

    (
        "The Silent Server",
        "Corporate Sabotage / Data Theft",
        "TechNova's central server shut down at 2:35 AM. Minutes earlier, confidential client data had been copied and transferred to an unknown external IP address. The security dashboard showed no unauthorized login because the commands used valid stored administrator credentials. ",
        "TechNova Software Company, Dhaka",
        "28 October 2026"
    ),

    (
        "The 2-Minute Alibi",
        "Murder",
        "someone had entered from outside. The electronic lock showed a valid room-entry event at 10:08 PM, but the event was later found to have been generated remotely. ",
        "Room 707, Grand Imperial Hotel, Dhaka",
        "30 October 2026"
    ),

    (
        "The Deadly Prescription",
        "Homicide / Murder",
        "A prominent cardiologist, Dr. Tariq Hasan was found dead in his private office at Care Central Hospital. Death was caused by an acute lethal dose of Potassium Chloride injected directly into his IV drip during or immediately following a private evening patient consultation.",
        "Care Central Hospital, Gulshan, Dhaka",
        "8 November 2026"
    ),

    (
        "The Poisoned Birthday Slice",
        "Attempted Homicide / Poisoning",
        "During Lily's 25th birthday celebration at The Grand Orchid Banquets, Lily collapsed shortly after eating the first slice of her custom red velvet birthday cake.Toxicology confirmed the presence of a fast-acting organophosphate pesticide mixed into the strawberry topping layer.",
        "The Grand Orchid Banquets, Banani, Dhaka",
        "9 November 2026"
    ),

    (
        "The Stolen Land Deed",
        "Grand Theft / Burglary",
        "Original ancestral land deeds worth over 50 million BDT disappeared from the heavy iron safe in the study of retired patriarch Chowdhury Jalal Uddin. The safe showed no signs of forced entry, indicating that a key or master combination was used.",
        "Chowdhury Estate, Sector 3, Uttara, Dhaka",
        "8 November 2026"
    )
]

#           INSERT ALL 10 CASES

def insert_cases():

    existing_cases = get_all_cases()

    if existing_cases:
        print("Cases already exist in database.")
        print("Do not insert the same cases again.")
        return

    for case in CASES_DATA:
        case_id = add_case(
            case[0],
            case[1],
            case[2],
            case[3],
            case[4]
        )

        print(f"Case inserted successfully. Case ID: {case_id}")

    print("Total cases:", len(CASES_DATA))


#             GET ALL CASES

def get_case_list():
    return get_all_cases()


#             GET CASE DETAILS

def get_case_details(case_id):

    cases = get_all_cases()

    for case in cases:

        if case[0] == case_id:

            return {
                "case_id": case[0],
                "case_title": case[1],
                "case_type": case[2],
                "description": case[3],
                "location": case[4],
                "incident_date": case[5],
                "status": case[6]
            }

    return None


#          INSERT ONE CASE SOLUTION


def insert_case_solution(case_id, culprit_name, explanation):

    existing_solution = get_solution(case_id)

    if existing_solution:
        print(f"Solution already exists for Case {case_id}.")
        return False

    suspects = get_all_suspects(case_id)

    culprit_id = None

    for suspect in suspects:

        # Suspect tuple:
        # (suspect_id, case_id, suspect_name, age, occupation, address)

        if suspect[2].strip().lower() == culprit_name.strip().lower():
            culprit_id = suspect[0]
            break

    if culprit_id is None:
        print(f"Culprit not found for Case {case_id}: {culprit_name}")
        return False

    add_solution(
        case_id,
        culprit_id,
        explanation
    )

    print(f"Solution inserted successfully for Case {case_id}.")
    return True


#          ALL 10 CASE SOLUTIONS

SOLUTIONS_DATA = [

    (
        1,
        "Samiha Rahman",
        "The display case was opened at 11:47 PM using Samiha's access card. Her 11:20 PM exit record proves only that her card was used, not that she physically left. A replacement necklace box was found in her assigned locked drawer, which was accessed using her staff code shortly after the theft."
    ),

    (
        2,
        "Samira Karim",
        "The 9:38 PM laptop message was scheduled earlier and does not prove that Rehan was alive at that time. Samira's building access record places her at the building at 9:12 PM, within the estimated time of death. The study-room door was locked using her personal access code at 9:18 PM. Her statement that she returned at 10:30 PM conflicts with these records."
    ),

    (
        3,
        "Rafi Ahmed",
        "The digital lock was opened with the master code at 9:27 PM. Only Ayesha Rahman and Rafi Ahmed were authorized to use that code. Rafi's duty note recorded a corridor issue at 9:26 PM, immediately before the lock was opened. The investigation identifies Rafi Ahmed as the culprit."
    ),

    (
        4,
        "Tuhin Ahmed",
        "The project room was opened at 6:42 PM using temporary access card T-17, assigned to Tuhin Ahmed. CCTV showed a person carrying a green folder entering the corridor at 6:43 PM. A torn paper piece found beside the cabinet matched the damaged corner of Tuhin's folder. The gate register also showed that Tuhin left at 7:05 PM, not 6:20 PM as he claimed."
    ),

    (
        5,
        "Nadia Karim",
        "The display case was opened at 8:24 PM using pass E-17, assigned to Nadia Karim. The pass had not been returned before that time. Nadia claimed she remained at reception, but the receptionist's note recorded that she left the desk shortly after 8:20 PM. The other suspects had records supporting their locations during the relevant period."
    ),

    (
        6,
        "Rifat Ahmed",
        "The administrator account used for the shutdown belonged to Arman, but the execution history links the malicious script and server commands to Rifat's remote workstation. The script used stored administrator credentials, explaining why a valid administrator account appeared in the server log. The network log confirms the data transfer."
    ),

    (
        7,
        "Shafin Malik",
        "The apparent Tania keycard entry was generated remotely through the hotel's access-control console. The console session used Shafin's manager credentials. The same credentials were used to disable the balcony sensor, and the maintenance ticket was falsely closed as routine testing. Service-corridor footage supports the system records."
    ),

    (
        8,
        "Dr. Faisal Mahmud",
        "The lethal cardiac event occurred at 7:34 PM. Imran had already left the hospital, while Nusrat's alibi was supported by video footage. Dr. Faisal used Nusrat's borrowed keycard to obtain Potassium Chloride at 7:22 PM and entered Dr. Hasan's office at 7:30 PM. The investigation identifies him as the culprit."
    ),

    (
        9,
        "Samira Haque",
        "The pesticide was concentrated exclusively in the strawberry glaze. Bakery CCTV showed Samira preparing the glaze and placing a marked container in her delivery kit. The pantry remained locked after delivery, while Tariq and Nadia had no opportunity to access the sealed cake. An empty pesticide vial was recovered behind Samira's bakery shop."
    ),

    (
        10,
        "Khorshed Alam",
        "Fresh silicone wax was found in the drawer where the original safe key was stored, indicating that a duplicate key had been made. The three brothers were accounted for on CCTV. A duplicate key and the original land deeds were found concealed in Khorshed's staff locker, alongside contact logs with an illegal deed forgery ring."
    )
]


#         INSERT ALL CASE SOLUTIONS

def insert_all_case_solutions():

    for solution in SOLUTIONS_DATA:

        case_id = solution[0]
        culprit_name = solution[1]
        explanation = solution[2]

        insert_case_solution(
            case_id,
            culprit_name,
            explanation
        )
