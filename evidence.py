from database import (
    create_tables,
    add_evidence,
    get_evidence_by_case,
    update_evidence,
    delete_evidence,
    get_all_cases
)


# ==========================================================
# CASE EVIDENCE DATA
# Based on CaseClosed_Revised_Cases.pdf
# Total: 58 Evidence Records
# ==========================================================

CASE_EVIDENCE = {

    # ======================================================
    # CASE 001 - THE 11:47 PM DISAPPEARANCE
    # ======================================================
    "CASE-001": [
        (
            "Display Case Access Log",
            "Digital Record",
            "The display case was opened at 11:47 PM using Samiha's access card.",
            "16 Oct 2026"
        ),
        (
            "CCTV Recording",
            "Video Record",
            "The corridor CCTV recording from 11:40 PM to 11:55 PM is missing.",
            "16 Oct 2026"
        ),
        (
            "Security Console Audit",
            "Digital Record",
            "The CCTV system was manually paused at 11:42 PM using a session authenticated in the security room.",
            "16 Oct 2026"
        ),
        (
            "Photographer's Image",
            "Digital Evidence",
            "A photograph recorded by Tasrif's camera at 11:30 PM shows the reflection of a person wearing Samiha's distinctive silver bracelet. The original image metadata confirms 11:30 PM.",
            "16 Oct 2026"
        ),
        (
            "Gallery Exit Log",
            "Written Record",
            "Samiha's access card registered an exit at 11:20 PM. The log records card use, not the identity of the person carrying it.",
            "16 Oct 2026"
        ),
        (
            "Office Search",
            "Physical",
            "A replacement necklace box was found in a locked drawer assigned to Samiha. The drawer was accessed with her staff code shortly after 11:50 PM.",
            "16 Oct 2026"
        ),
        (
            "Inventory Check",
            "Written Evidence",
            "The original necklace was absent; the replacement box contained a replica with a different serial number.",
            "16 Oct 2026"
        )
    ],


    # ======================================================
    # CASE 002 - THE LAST MESSAGE
    # ======================================================
    "CASE-002": [
        (
            "Medical Report",
            "Medical Record",
            "The estimated time of death is between 9:05 PM and 9:25 PM.",
            "22 Oct 2026"
        ),
        (
            "Laptop Message Metadata",
            "Digital Record",
            "The 9:38 PM message was scheduled earlier. The timestamp records its delivery time, not the time it was typed.",
            "23 Oct 2026"
        ),
        (
            "Building Elevator Log",
            "Digital Record",
            "Samira's building access record shows her returning at 9:12 PM.",
            "23 Oct 2026"
        ),
        (
            "Office CCTV",
            "Video Record",
            "Imran's office CCTV confirms he remained at work from 8:50 PM to 10:00 PM.",
            "23 Oct 2026"
        ),
        (
            "University Access and CCTV",
            "Digital / Video Record",
            "Nusrat's access log and laboratory camera confirm she remained on campus until 9:40 PM.",
            "23 Oct 2026"
        ),
        (
            "Smart-Home Audit",
            "Digital Record",
            "The study-room door was manually locked at 9:18 PM using Samira's personal access code.",
            "23 Oct 2026"
        ),
        (
            "Scene Evidence",
            "Physical Evidence",
            "A broken glass fragment near the study desk matches a glass from the apartment's kitchen. This establishes a likely source for the fragment but does not independently identify who broke it.",
            "22 Oct 2026"
        )
    ],


    # ======================================================
    # CASE 003 - THE VANISHING DIAMOND
    # ======================================================
    "CASE-003": [
        (
            "Digital Lock Record",
            "Digital Record",
            "The master code opened the display case at 9:27 PM.",
            "6 Nov 2026"
        ),
        (
            "Security Register",
            "Written Record",
            "Only Ayesha Rahman and Rafi Ahmed were authorized to use the master code.",
            "6 Nov 2026"
        ),
        (
            "CCTV Footage",
            "Video Record",
            "A person approached the display case around 9:25 PM; the face was not clearly identified.",
            "6 Nov 2026"
        ),
        (
            "Photography Metadata",
            "Digital Record",
            "Meera Khan's camera had a photo at 9:28 PM showing the wall clock and main exhibition hall.",
            "6 Nov 2026"
        ),
        (
            "Security Duty Note",
            "Written Record",
            "Rafi Ahmed recorded a security issue in the north corridor at 9:26 PM, one minute before the display case opened.",
            "6 Nov 2026"
        )
    ],


    # ======================================================
    # CASE 004 - THE MISSING PROTOTYPE
    # ======================================================
    "CASE-004": [
        (
            "Access Card Log",
            "Digital Record",
            "The project room door opened at 6:42 PM using temporary access card T-17 issued to Tuhin Ahmed.",
            "13 Oct 2026"
        ),
        (
            "Hallway CCTV",
            "Video Record",
            "At 6:43 PM a person carrying a green folder entered the project room corridor. The face was partly hidden and the folder had a torn lower corner.",
            "13 Oct 2026"
        ),
        (
            "Torn Paper Piece",
            "Physical Evidence",
            "A small torn piece of green folder paper was found beside the cabinet. Its torn edge matched the missing corner of Tuhin Ahmed's green folder.",
            "13 Oct 2026"
        ),
        (
            "Main Gate Register",
            "Written Record",
            "Tuhin left the institute at 7:05 PM, not 6:20 PM as claimed.",
            "13 Oct 2026"
        ),
        (
            "Meeting Attendance Record",
            "Written Record",
            "Sana attended the Room 105 meeting from 6:35 PM to 7:00 PM. The organizer confirmed her attendance.",
            "13 Oct 2026"
        ),
        (
            "Server Room Entry Log",
            "Digital Record",
            "Imran used his own access card to enter the server room at 6:30 PM and exited at 7:02 PM.",
            "13 Oct 2026"
        )
    ],


    # ======================================================
    # CASE 005 - THE MISSING BLUEPRINT
    # ======================================================
    "CASE-005": [
        (
            "Display Case Log",
            "Digital Record",
            "The display case was opened at 8:24 PM using temporary staff access card E-17.",
            "19 Oct 2026"
        ),
        (
            "Staff Pass Register",
            "Written Record",
            "Pass E-17 was issued to Nadia Karim and was not recorded returned before 8:40 PM.",
            "19 Oct 2026"
        ),
        (
            "Workshop Entry Record",
            "Digital Record",
            "Imran's staff card was used to enter the workshop at 8:17 PM. The workshop is in a separate building about five minutes from the display room.",
            "19 Oct 2026"
        ),
        (
            "Camera Photographs",
            "Digital Evidence",
            "Tania's camera photos were taken at 8:19 PM and 8:28 PM, showing the main hall clock and exhibition stage.",
            "19 Oct 2026"
        ),
        (
            "Security Patrol Sheet",
            "Written Record",
            "Farhan's east-entrance patrol was recorded at 8:20 PM. A visitor's signed assistance form confirms he helped at the east entrance at 8:23 PM.",
            "19 Oct 2026"
        ),
        (
            "Reception Desk Note",
            "Written Record",
            "The receptionist noted that Nadia left the desk briefly to check a pass issue shortly after 8:20 PM.",
            "19 Oct 2026"
        )
    ],


    # ======================================================
    # CASE 006 - THE SILENT SERVER
    # ======================================================
    "CASE-006": [
        (
            "Server Command Log",
            "Digital Record",
            "A shutdown command was executed at 2:35 AM using Arman's administrator account.",
            "28 Oct 2026"
        ),
        (
            "Server-Room Access Log",
            "Digital Record",
            "Arman's employee card was used to enter the server room at 2:20 AM.",
            "28 Oct 2026"
        ),
        (
            "Corridor CCTV",
            "Video Record",
            "A person entered the server room wearing an employee uniform. The person's face is not visible.",
            "28 Oct 2026"
        ),
        (
            "Network Transfer Log",
            "Digital Record",
            "A large data transfer to an external IP address began at 2:41 AM.",
            "29 Oct 2026"
        ),
        (
            "Arman's Home Router Log",
            "Digital Record",
            "Arman's home router shows his laptop connected to his home Wi-Fi from 2:15 AM to 2:50 AM.",
            "29 Oct 2026"
        ),
        (
            "Rifat's Workstation",
            "Digital Evidence",
            "A script capable of sending server commands using stored administrator credentials was found on Rifat's remote workstation.",
            "29 Oct 2026"
        ),
        (
            "Security Dashboard Audit",
            "Digital Record",
            "At 2:43 AM, the network-transfer alert was manually marked as \"maintenance activity\" from Maya's dashboard account.",
            "29 Oct 2026"
        ),
        (
            "Script Execution History",
            "Digital Record",
            "The execution history records the malicious script running on Rifat's workstation. The script log records the shutdown and data-transfer commands initiated by that workstation.",
            "29 Oct 2026"
        )
    ],


    # ======================================================
    # CASE 007 - THE 2-MINUTE ALIBI
    # ======================================================
    "CASE-007": [
        (
            "Room Lock Record",
            "Digital Record",
            "A valid room-entry event was recorded at 10:08 PM.",
            "30 Oct 2026"
        ),
        (
            "Lobby CCTV",
            "Video Record",
            "Rayan is visible leaving the hotel at 9:57 PM.",
            "30 Oct 2026"
        ),
        (
            "Reception Login Record",
            "Digital Record",
            "Tania's reception account remained active from 9:45 PM to 10:20 PM. This supports her presence at reception but does not prove she never left the desk.",
            "30 Oct 2026"
        ),
        (
            "Keycard Account",
            "Digital Record",
            "The 10:08 PM transaction was associated with Tania's employee keycard account.",
            "30 Oct 2026"
        ),
        (
            "Balcony Sensor Audit",
            "Digital Record",
            "The balcony door sensor was disabled at 9:50 PM using Shafin's maintenance credentials.",
            "31 Oct 2026"
        ),
        (
            "Remote Transaction Audit",
            "Digital Record",
            "A backup access log shows the 10:08 PM keycard transaction was generated remotely by the hotel's access-control console, not by physically presenting Tania's card at the room.",
            "31 Oct 2026"
        ),
        (
            "Administrator Session Log",
            "Digital Record",
            "The access-control console was logged in with Shafin's manager credentials when the remote transaction was generated.",
            "31 Oct 2026"
        ),
        (
            "Service Corridor CCTV",
            "Video Record",
            "A person wearing the hotel manager's uniform is recorded entering the seventh-floor service corridor shortly before 10:08 PM. The face is not clear, so the footage is corroborative rather than conclusive.",
            "31 Oct 2026"
        ),
        (
            "Maintenance Ticket History",
            "Digital Record",
            "Shafin's account disabled the balcony sensor and then closed the maintenance ticket as \"routine testing,\" although no scheduled test was approved.",
            "31 Oct 2026"
        )
    ],


    # ======================================================
    # CASE 008 - THE DEADLY PRESCRIPTION
    # ======================================================
    "CASE-008": [
        (
            "Syringe & Vial",
            "Physical Evidence",
            "An empty 10ml syringe containing trace Potassium Chloride was recovered from the office hazardous bio-bin.",
            "8 Nov 2026"
        ),
        (
            "Keycard Access Log",
            "Digital Record",
            "Keycard #04 (Nusrat) accessed the drug storage at 7:22 PM and the office suite at 7:31 PM.",
            "8 Nov 2026"
        ),
        (
            "Corridor CCTV",
            "Video Record",
            "Imran exited Dr. Hasan's office at 7:28 PM, and Dr. Faisal entered the consultation anteroom at 7:30 PM.",
            "8 Nov 2026"
        ),
        (
            "Smart Watch Data",
            "Digital Record",
            "Dr. Hasan's heart-rate monitor recorded fatal arrhythmia beginning at 7:34 PM.",
            "9 Nov 2026"
        ),
        (
            "Dispensary Register",
            "Written Record",
            "Potassium Chloride ampoules were audited; one unit was unaccounted for under Nurse Nusrat's shift log.",
            "9 Nov 2026"
        )
    ],


    # ======================================================
    # CASE 009 - THE POISONED BIRTHDAY SLICE
    # ======================================================
    "CASE-009": [
        (
            "Cake Residue Sample",
            "Forensic Sample",
            "Toxicology showed pesticide contamination concentrated in the strawberry glaze on the slice served to Lily.",
            "9 Nov 2026"
        ),
        (
            "Bakery CCTV Footage",
            "Video Record",
            "Samira was recorded preparing strawberry glaze at 4:15 PM and placing the marked container separately in the delivery kit.",
            "9 Nov 2026"
        ),
        (
            "Venue Pantry Log",
            "Written Record",
            "Nadia Islam logged the cake delivery at 6:30 PM; the pantry remained locked until 7:25 PM.",
            "9 Nov 2026"
        ),
        (
            "Fingerprint Analysis",
            "Forensic Evidence",
            "Tariq Aziz's fingerprints were found on the water tumbler, with none on the cake box or dessert utensils.",
            "9 Nov 2026"
        ),
        (
            "Pesticide Container",
            "Physical Evidence",
            "An empty agricultural pesticide vial was recovered from the trash receptacle behind Samira's bakery shop.",
            "9 Nov 2026"
        )
    ],


    # ======================================================
    # CASE 010 - THE STOLEN LAND DEED
    # ======================================================
    "CASE-010": [
        (
            "Safe Key Impression",
            "Forensic Sample",
            "Fresh jeweler's silicone wax was found inside the study desk drawer where the main safe key was stored.",
            "9 Nov 2026"
        ),
        (
            "Estate CCTV Footage",
            "Video Record",
            "Asif, Nabil, and Zubair were recorded in the dining hall between 7:00 PM and 8:15 PM, with Zubair stepping away for 5 minutes at 7:15 PM.",
            "9 Nov 2026"
        ),
        (
            "Dusting Cloth & Key",
            "Physical Evidence",
            "A duplicate safe key wrapped in a cleaning cloth was discovered hidden inside a supply locker in the staff quarter.",
            "9 Nov 2026"
        ),
        (
            "Pawn Broker Contact Log",
            "Digital Record",
            "Phone records revealed multiple encrypted calls between an unlisted broker and Khorshed Alam over the past two weeks.",
            "9 Nov 2026"
        )
    ]
}


def _resolve_case_id(raw_id: str) -> str:
    """Allow user/data IDs like '1', '001', or 'CASE-001' to match CASE_EVIDENCE."""
    cleaned = str(raw_id).strip().upper()
    if cleaned in CASE_EVIDENCE:
        return cleaned
    if cleaned.isdigit():
        formatted = f"CASE-{int(cleaned):03d}"
        if formatted in CASE_EVIDENCE:
            return formatted
    return str(raw_id).strip()


# ==========================================================
# ADD NEW EVIDENCE
# ==========================================================

def add_new_evidence():
    print("\n========== ADD NEW EVIDENCE ==========")

    case_id = input("Enter Case ID (e.g., CASE-001): ").strip()

    cases = get_all_cases()
    valid_case_ids = {case["case_id"] for case in cases}

    if case_id not in valid_case_ids:
        print("Error: Case ID does not exist.")
        return

    evidence_name = input("Enter Evidence Name: ").strip()
    evidence_type = input("Enter Evidence Type: ").strip()
    description = input("Enter Description: ").strip()
    collected_date = input("Enter Collected Date: ").strip()

    if not evidence_name:
        print("Evidence name cannot be empty.")
        return

    new_id = add_evidence(case_id, {
        "evidence_name": evidence_name,
        "evidence_type": evidence_type or None,
        "description": description or None,
        "collected_date": collected_date or None
    })
    print(f"Evidence added successfully (ID: {new_id}).")


# ==========================================================
# VIEW EVIDENCE FOR ONE CASE
# ==========================================================

def view_evidence():
    print("\n========== VIEW EVIDENCE ==========")

    case_id = input("Enter Case ID (e.g., CASE-001): ").strip()

    cases = get_all_cases()
    valid_case_ids = {case["case_id"] for case in cases}

    if case_id not in valid_case_ids:
        print("Error: Case ID does not exist.")
        return

    evidence_list = get_evidence_by_case(case_id)

    if not evidence_list:
        print("No evidence found for this case.")
        return

    print("\nCase ID:", case_id)
    print("-" * 80)

    for evidence in evidence_list:
        print(f"Evidence ID    : {evidence['evidence_id']}")
        print(f"Case ID        : {evidence['case_id']}")
        print(f"Evidence Name  : {evidence['evidence_name']}")
        print(f"Evidence Type  : {evidence['evidence_type']}")
        print(f"Description    : {evidence['description']}")
        print(f"Collected Date : {evidence['collected_date']}")
        print("-" * 80)


# ==========================================================
# UPDATE EXISTING EVIDENCE
# ==========================================================

def update_existing_evidence():
    print("\n========== UPDATE EVIDENCE ==========")

    try:
        evidence_id = int(input("Enter Evidence ID: ").strip())

        evidence_name = input("Enter New Evidence Name: ").strip()
        evidence_type = input("Enter New Evidence Type: ").strip()
        description = input("Enter New Description: ").strip()
        collected_date = input("Enter New Collected Date: ").strip()

        if not evidence_name:
            print("Evidence name cannot be empty.")
            return

        updated = update_evidence(evidence_id, {
            "evidence_name": evidence_name,
            "evidence_type": evidence_type or None,
            "description": description or None,
            "collected_date": collected_date or None
        })
        if updated:
            print("Evidence updated successfully.")
        else:
            print("Evidence ID not found.")

    except ValueError:
        print("Invalid Evidence ID. Please enter a number.")


# ==========================================================
# DELETE EXISTING EVIDENCE
# ==========================================================

def delete_existing_evidence():
    print("\n========== DELETE EVIDENCE ==========")

    try:
        evidence_id = int(input("Enter Evidence ID: ").strip())

        confirmation = input(
            "Are you sure you want to delete this evidence? (yes/no): "
        ).strip().lower()

        if confirmation == "yes":
            if delete_evidence(evidence_id):
                print("Evidence deleted successfully.")
            else:
                print("Evidence ID not found.")
        else:
            print("Delete operation cancelled.")

    except ValueError:
        print("Invalid Evidence ID. Please enter a number.")


# ==========================================================
# LOAD EVIDENCE FOR ONE CASE
# ==========================================================

def load_case_evidence(case_id):
    dict_key = _resolve_case_id(case_id)

    if dict_key not in CASE_EVIDENCE:
        print(f"No predefined evidence found for Case {case_id}.")
        return

    cases = get_all_cases()
    valid_case_ids = {case["case_id"] for case in cases}

    target_db_id = str(case_id).strip()
    if target_db_id not in valid_case_ids and dict_key in valid_case_ids:
        target_db_id = dict_key

    if target_db_id not in valid_case_ids:
        print(f"Case {target_db_id} does not exist in the database.")
        return

    existing_evidence = get_evidence_by_case(target_db_id)

    existing_names = {
        evidence["evidence_name"].strip().lower()
        for evidence in existing_evidence
    }

    added_count = 0

    for evidence_name, evidence_type, description, collected_date in CASE_EVIDENCE[dict_key]:
        if evidence_name.strip().lower() in existing_names:
            continue

        add_evidence(target_db_id, {
            "evidence_name": evidence_name,
            "evidence_type": evidence_type,
            "description": description,
            "collected_date": collected_date
        })
        added_count += 1

    print(f"{target_db_id}: {added_count} new evidence record(s) added.")


# ==========================================================
# LOAD ALL 10 CASES' EVIDENCE
# ==========================================================

def load_all_case_evidence():
    print("\n==========================================")
    print("      LOADING ALL CASE EVIDENCE")
    print("==========================================")

    for case_id in CASE_EVIDENCE:
        load_case_evidence(case_id)

    print("\nAll available case evidence has been loaded.")


# ==========================================================
# VIEW ALL EVIDENCE
# ==========================================================

def view_all_evidence():
    print("\n==========================================")
    print("        ALL CASE EVIDENCE")
    print("==========================================")

    cases = get_all_cases()

    if not cases:
        print("No cases found in the database.")
        return

    total_evidence = 0

    for case in cases:
        case_id = case["case_id"]
        case_title = case["case_title"]

        evidence_list = get_evidence_by_case(case_id)

        if not evidence_list:
            continue

        print("\n" + "=" * 80)
        print(f"CASE ID: {case_id}")
        print(f"CASE TITLE: {case_title}")
        print("=" * 80)

        for evidence in evidence_list:
            print(f"\nEvidence ID    : {evidence['evidence_id']}")
            print(f"Evidence Name  : {evidence['evidence_name']}")
            print(f"Evidence Type  : {evidence['evidence_type']}")
            print(f"Description    : {evidence['description']}")
            print(f"Collected Date : {evidence['collected_date']}")
            print("-" * 80)

            total_evidence += 1

    print("\nTotal Evidence Records:", total_evidence)


# ==========================================================
# EVIDENCE MENU
# ==========================================================

def evidence_menu():
    while True:
        print("\n")
        print("==========================================")
        print("        CASECLOSED - EVIDENCE")
        print("==========================================")
        print("1. Load All Case Evidence")
        print("2. View Evidence")
        print("3. Add New Evidence")
        print("4. Update Evidence")
        print("5. Delete Evidence")
        print("6. View All Evidence")
        print("7. Exit")
        print("==========================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            load_all_case_evidence()

        elif choice == "2":
            view_evidence()

        elif choice == "3":
            add_new_evidence()

        elif choice == "4":
            update_existing_evidence()

        elif choice == "5":
            delete_existing_evidence()

        elif choice == "6":
            view_all_evidence()

        elif choice == "7":
            print("\nExiting Evidence Module...")
            break

        else:
            print("Invalid choice. Please try again.")


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    create_tables()
    evidence_menu()