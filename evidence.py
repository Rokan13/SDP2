
from database import (
    connect_db,
    create_tables,
    add_evidence,
    get_all_evidence,
    update_evidence,
    delete_evidence,
    get_all_cases
)


# ==========================================
#              CASECLOSED
#               EVIDENCE
# ==========================================


# Evidence format:
# (evidence_name, evidence_type, description, collected_date)

CASE_EVIDENCE = {

    # ======================================
    # CASE 001 - THE 11:47 PM DISAPPEARANCE
    # ======================================

    1: [
        (
            "Display Case Access Log",
            None,
            "Display case opened at 11:47 PM using Samiha's access card.",
            None
        ),
        (
            "CCTV Recording",
            None,
            "Corridor CCTV recording from 11:40 PM to 11:55 PM is missing.",
            None
        ),
        (
            "Security Console Audit",
            None,
            "CCTV system was manually paused at 11:42 PM using a session authenticated in the security room.",
            None
        ),
        (
            "Photographer's Image",
            None,
            "Tasrif's camera photo at 11:30 PM shows the reflection of a person wearing Samiha's distinctive silver bracelet. Original metadata confirms the time.",
            None
        ),
        (
            "Gallery Exit Log",
            None,
            "Samiha's access card registered an exit at 11:20 PM. The record confirms card use, not the identity of the person carrying it.",
            None
        ),
        (
            "Office Search",
            None,
            "A replacement necklace box was found in a locked drawer assigned to Samiha. The drawer was opened using her staff code shortly after 11:50 PM.",
            None
        ),
        (
            "Inventory Check",
            None,
            "The original necklace was absent. The replacement box contained a replica with a different serial number.",
            None
        )
    ],


    # ======================================
    # CASE 002 - THE LAST MESSAGE
    # ======================================

    2: [
        (
            "Medical Report",
            None,
            "Estimated time of death was between 9:05 PM and 9:25 PM.",
            None
        ),
        (
            "Laptop Message Metadata",
            None,
            "The 9:38 PM message had been scheduled earlier. Its timestamp represents delivery time, not typing time.",
            None
        ),
        (
            "Building Elevator Log",
            None,
            "Samira's building access record shows her return at 9:12 PM.",
            None
        ),
        (
            "Office CCTV",
            None,
            "Imran's office CCTV confirms that he remained at work from 8:50 PM to 10:00 PM.",
            None
        ),
        (
            "University Access and CCTV",
            None,
            "Nusrat's access log and laboratory camera confirm that she remained on campus until 9:40 PM.",
            None
        ),
        (
            "Smart-Home Audit",
            None,
            "Study-room door was manually locked at 9:18 PM using Samira's personal access code.",
            None
        ),
        (
            "Scene Evidence",
            None,
            "A broken glass fragment near the study desk matches a glass from the apartment kitchen. It establishes the likely source but not who broke it.",
            None
        )
    ],


    # ======================================
    # CASE 003 - THE VANISHING DIAMOND
    # ======================================

    3: [
        (
            "Digital Lock Record",
            "Digital Record",
            "Master code opened the display case at 9:27 PM.",
            "2026-11-06"
        ),
        (
            "Security Register",
            "Written Record",
            "Only Ayesha Rahman and Rafi Ahmed were authorized to use the master code.",
            "2026-11-06"
        ),
        (
            "CCTV Footage",
            "Video Record",
            "A person approached the display case around 9:25 PM. The face was not clearly identified.",
            "2026-11-06"
        ),
        (
            "Photography Metadata",
            "Digital Record",
            "Meera Khan's camera had a photo at 9:28 PM showing the wall clock and main exhibition hall.",
            "2026-11-06"
        ),
        (
            "Security Duty Note",
            "Written Record",
            "Rafi Ahmed recorded a security issue in the north corridor at 9:26 PM, one minute before the display case opened.",
            "2026-11-06"
        )
    ],


    # ======================================
    # CASE 004 - THE MISSING PROTOTYPE
    # ======================================

    4: [
        (
            "Access Card Log",
            "Digital Record",
            "Project room door opened at 6:42 PM using temporary access card T-17 issued to Tuhin Ahmed.",
            "2026-10-13"
        ),
        (
            "Hallway CCTV",
            "Video Record",
            "At 6:43 PM, a person carrying a green folder entered the project room corridor. The face was partly hidden and the folder had a torn lower corner.",
            "2026-10-13"
        ),
        (
            "Torn Paper Piece",
            "Physical Evidence",
            "A small torn piece of green folder paper was found beside the cabinet. Its torn edge matched the missing corner of Tuhin Ahmed's green folder.",
            "2026-10-13"
        ),
        (
            "Main Gate Register",
            "Written Record",
            "Tuhin left the institute at 7:05 PM, not 6:20 PM as he claimed.",
            "2026-10-13"
        ),
        (
            "Meeting Attendance Record",
            "Written Record",
            "Sana attended the Room 105 meeting from 6:35 PM to 7:00 PM. The organizer confirmed her attendance.",
            "2026-10-13"
        ),
        (
            "Server Room Entry Log",
            "Digital Record",
            "Imran used his own access card to enter the server room at 6:30 PM and exited at 7:02 PM.",
            "2026-10-13"
        )
    ],


    # ======================================
    # CASE 005 - THE MISSING BLUEPRINT
    # ======================================

    5: [
        (
            "Display Case Log",
            "Digital Record",
            "Display case opened at 8:24 PM using temporary staff access card E-17.",
            "2026-10-19"
        ),
        (
            "Staff Pass Register",
            "Written Record",
            "Pass E-17 was issued to Nadia Karim and was not recorded as returned before 8:40 PM.",
            "2026-10-19"
        ),
        (
            "Workshop Entry Record",
            "Digital Record",
            "Imran's staff card was used to enter the workshop at 8:17 PM. The workshop is in a separate building about five minutes from the display room.",
            "2026-10-19"
        ),
        (
            "Camera Photographs",
            "Digital Evidence",
            "Tania's camera photographs were taken at 8:19 PM and 8:28 PM, showing the main hall clock and exhibition stage.",
            "2026-10-19"
        ),
        (
            "Security Patrol Sheet",
            "Written Record",
            "Farhan's east-entrance patrol was recorded at 8:20 PM. A visitor's signed assistance form confirms he helped at the east entrance at 8:23 PM.",
            "2026-10-19"
        ),
        (
            "Reception Desk Note",
            "Written Record",
            "The receptionist noted that Nadia left the desk briefly to check a pass issue shortly after 8:20 PM.",
            "2026-10-19"
        )
    ],


    # ======================================
    # CASE 006 - THE SILENT SERVER
    # ======================================

    6: [
        (
            "Server Command Log",
            "Digital Record",
            "A shutdown command was recorded at 2:35 AM using Arman's administrator account.",
            None
        ),
        (
            "Server-Room Access Log",
            "Digital Record",
            "Arman's employee card was used to enter the server room at 2:20 AM.",
            None
        ),
        (
            "Corridor CCTV",
            "Video Record",
            "A person wearing an employee uniform entered the server room. The face was not visible.",
            None
        ),
        (
            "Network Transfer Log",
            "Digital Record",
            "A large data transfer to an external IP address began at 2:41 AM.",
            None
        ),
        (
            "Arman's Home Router Log",
            "Digital Record",
            "Arman's home router shows a laptop connected to home Wi-Fi from 2:15 AM to 2:50 AM.",
            None
        ),
        (
            "Rifat's Workstation",
            "Digital Evidence",
            "A script capable of sending server commands using stored administrator credentials was found on Rifat's remote workstation.",
            None
        ),
        (
            "Security Dashboard Audit",
            "Digital Record",
            "At 2:43 AM, a network transfer alert was manually marked as maintenance activity from Maya's dashboard account.",
            None
        ),
        (
            "Script Execution History",
            "Digital Record",
            "Execution history records a script running on Rifat's workstation. Its log records shutdown and data-transfer commands initiated by that workstation.",
            None
        )
    ],


    # ======================================
    # CASE 007 - THE 2-MINUTE ALIBI
    # ======================================

    7: [
        (
            "Room Lock Record",
            "Digital Record",
            "A valid room-entry event was recorded at 10:08 PM.",
            None
        ),
        (
            "Lobby CCTV",
            "Video Record",
            "Rayan was visible leaving the hotel at 9:57 PM.",
            None
        ),
        (
            "Reception Login Record",
            "Digital Record",
            "Tania's reception account was active from 9:45 PM to 10:20 PM. This supports reception presence but does not prove she never left.",
            None
        ),
        (
            "Keycard Account",
            "Digital Record",
            "The 10:08 PM transaction was associated with Tania's employee keycard account.",
            None
        ),
        (
            "Balcony Sensor Audit",
            "Digital Record",
            "The balcony door sensor was disabled at 9:50 PM using Shafin's maintenance credentials.",
            None
        ),
        (
            "Remote Transaction Audit",
            "Digital Record",
            "Backup access log shows that the 10:08 PM keycard transaction was generated remotely by the hotel's access-control console, not by physically presenting Tania's card at the room.",
            None
        ),
        (
            "Administrator Session Log",
            "Digital Record",
            "The access-control console was logged in using Shafin's manager credentials when the remote transaction was generated.",
            None
        ),
        (
            "Service Corridor CCTV",
            "Video Record",
            "A person in a hotel manager's uniform was recorded entering the seventh-floor service corridor shortly before 10:08 PM. The face was unclear.",
            None
        ),
        (
            "Maintenance Ticket History",
            "Digital Record",
            "Shafin's account disabled the balcony sensor and then closed the ticket as routine testing, although no scheduled test was approved.",
            None
        )
    ],


    # ======================================
    # CASE 008 - THE DEADLY PRESCRIPTION
    # ======================================

    8: [
        (
            "Syringe and Vial",
            "Physical Evidence",
            "An empty 10ml syringe containing traces of Potassium Chloride was recovered from the office hazardous bio-bin.",
            "2026-11-08"
        ),
        (
            "Keycard Access Log",
            "Digital Record",
            "Keycard number 04, assigned to Nusrat, accessed drug storage at 7:22 PM and the office suite at 7:31 PM.",
            "2026-11-08"
        ),
        (
            "Corridor CCTV",
            "Video Record",
            "Imran exited Dr. Hasan's office at 7:28 PM. Dr. Faisal entered the consultation anteroom at 7:30 PM.",
            "2026-11-08"
        ),
        (
            "Smart Watch Data",
            "Digital Record",
            "Dr. Hasan's heart-rate monitor recorded a fatal arrhythmia beginning at 7:34 PM.",
            "2026-11-09"
        ),
        (
            "Dispensary Register",
            "Written Record",
            "Potassium Chloride ampoules were audited. One unit was unaccounted for under Nurse Nusrat's shift log.",
            "2026-11-09"
        )
    ],


    # ======================================
    # CASE 009 - THE POISONED BIRTHDAY SLICE
    # ======================================

    9: [
        (
            "Cake Residue Sample",
            "Forensic Sample",
            "Toxicology showed pesticide contamination concentrated in the strawberry glaze on the slice served to Lily.",
            "2026-11-09"
        ),
        (
            "Bakery CCTV Footage",
            "Video Record",
            "Footage shows Samira preparing strawberry glaze at 4:15 PM and placing a marked container separately in her delivery kit.",
            "2026-11-09"
        ),
        (
            "Venue Pantry Log",
            "Written Record",
            "Nadia Islam logged cake delivery at 6:30 PM. The pantry remained locked until 7:25 PM.",
            "2026-11-09"
        ),
        (
            "Fingerprint Analysis",
            "Forensic Evidence",
            "Tariq Aziz's fingerprints were found on a water tumbler, but none were found on the cake box or dessert utensils.",
            "2026-11-09"
        ),
        (
            "Pesticide Container",
            "Physical Evidence",
            "An empty agricultural pesticide vial was recovered from a trash receptacle behind Samira's bakery shop.",
            "2026-11-09"
        )
    ],


    # ======================================
    # CASE 010 - THE STOLEN LAND DEED
    # ======================================

    # Case 010 evidence details need to be added
    # after checking the original PDF.
    10: []

}


# ==========================================
#              ADD EVIDENCE
# ==========================================

def add_new_evidence(
    case_id,
    evidence_name,
    evidence_type,
    description,
    collected_date
):

    add_evidence(
        case_id,
        evidence_name,
        evidence_type,
        description,
        collected_date
    )

    print("Evidence added successfully!")


# ==========================================
#              VIEW EVIDENCE
# ==========================================

def view_evidence(case_id):

    evidence_list = get_all_evidence(case_id)

    if not evidence_list:
        print("No evidence found for this case.")
        return

    print("\n========== EVIDENCE LIST ==========")
    print("Case ID:", case_id)

    for evidence in evidence_list:

        print("\nEvidence ID:", evidence[0])
        print("Evidence Name:", evidence[2])
        print("Evidence Type:", evidence[3] or "Not specified")
        print("Description:", evidence[4])
        print("Collected Date:", evidence[5] or "Not specified")


# ==========================================
#              UPDATE EVIDENCE
# ==========================================

def update_existing_evidence(
    evidence_id,
    evidence_name,
    evidence_type,
    description,
    collected_date
):

    update_evidence(
        evidence_id,
        evidence_name,
        evidence_type,
        description,
        collected_date
    )

    print("Evidence updated successfully!")


# ==========================================
#              DELETE EVIDENCE
# ==========================================

def delete_existing_evidence(evidence_id):

    delete_evidence(evidence_id)

    print("Evidence deleted successfully!")


# ==========================================
#          LOAD EVIDENCE FOR ONE CASE
# ==========================================

def load_case_evidence(case_id):

    if case_id not in CASE_EVIDENCE:
        print("Invalid Case ID.")
        return

    # Check whether the case exists in database
    all_cases = get_all_cases()

    existing_case_ids = [case[0] for case in all_cases]

    if case_id not in existing_case_ids:
        print("Case ID", case_id, "does not exist in database.")
        print("Please add the case before loading its evidence.")
        return

    evidence_records = CASE_EVIDENCE[case_id]

    if not evidence_records:
        print("No predefined evidence records available for Case", case_id)
        return

    # Get evidence already saved for this case
    existing_evidence = get_all_evidence(case_id)

    existing_names = [
        evidence[2].strip().lower()
        for evidence in existing_evidence
    ]

    added_count = 0
    skipped_count = 0

    for record in evidence_records:

        evidence_name, evidence_type, description, collected_date = record

        # Avoid duplicate evidence
        if evidence_name.strip().lower() in existing_names:
            skipped_count += 1
            continue

        add_evidence(
            case_id,
            evidence_name,
            evidence_type,
            description,
            collected_date
        )

        added_count += 1

    print("\nCase", case_id, "evidence loading completed!")
    print("New evidence added:", added_count)
    print("Duplicate evidence skipped:", skipped_count)


# ==========================================
#          LOAD EVIDENCE FOR ALL CASES
# ==========================================

def load_all_case_evidence():

    print("\n========== LOADING CASE EVIDENCE ==========")

    total_added = 0

    for case_id in range(1, 11):

        before = len(get_all_evidence(case_id))

        load_case_evidence(case_id)

        after = len(get_all_evidence(case_id))

        total_added += after - before

    print("\n==========================================")
    print("Evidence loading process finished!")
    print("Total new evidence added:", total_added)
    print("==========================================")


# ==========================================
#          DISPLAY ALL EVIDENCE
# ==========================================

def view_all_evidence():

    all_cases = get_all_cases()

    if not all_cases:
        print("No cases found in database.")
        return

    for case in all_cases:

        case_id = case[0]
        case_title = case[1]

        print("\n\n====================================")
        print("Case ID:", case_id)
        print("Case Title:", case_title)
        print("====================================")

        view_evidence(case_id)


# ==========================================
#               TEST MODULE
# ==========================================

if __name__ == "__main__":

    create_tables()

    print("\n========== CASECLOSED EVIDENCE MODULE ==========")

    print("\n1. Load evidence for all cases")
    print("2. View evidence of a case")
    print("3. Add new evidence")
    print("4. Update evidence")
    print("5. Delete evidence")
    print("6. View all evidence")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        load_all_case_evidence()

    elif choice == "2":

        case_id = int(input("Enter Case ID: "))
        view_evidence(case_id)

    elif choice == "3":

        case_id = int(input("Enter Case ID: "))
        name = input("Evidence Name: ")
        evidence_type = input("Evidence Type: ")
        description = input("Description: ")
        collected_date = input("Collected Date (YYYY-MM-DD): ")

        add_new_evidence(
            case_id,
            name,
            evidence_type or None,
            description,
            collected_date or None
        )

    elif choice == "4":

        evidence_id = int(input("Enter Evidence ID: "))
        name = input("New Evidence Name: ")
        evidence_type = input("New Evidence Type: ")
        description = input("New Description: ")
        collected_date = input("New Collected Date (YYYY-MM-DD): ")

        update_existing_evidence(
            evidence_id,
            name,
            evidence_type or None,
            description,
            collected_date or None
        )

    elif choice == "5":

        evidence_id = int(input("Enter Evidence ID: "))
        delete_existing_evidence(evidence_id)

    elif choice == "6":

        view_all_evidence()

    else:

        print("Invalid choice!")
