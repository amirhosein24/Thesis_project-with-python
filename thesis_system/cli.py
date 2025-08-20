import sys, os
from thesis_system import storage, models, utils

DATA_USERS = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")
DATA_COURSES = os.path.join(os.path.dirname(__file__), "..", "data", "courses.json")
DATA_SYSTEM = os.path.join(os.path.dirname(__file__), "..", "data", "system.json")
 
def load_all():
    users = storage.load("users.json")
    courses = storage.load("courses.json")
    system = storage.load("system.json")
    return users, courses, system

def save_system(system):
    storage.save("system.json", system)

def find_student_by_credentials(users, username, password):
    for s in users["students"]:
        if s["name"] == username and s["password"] == password:
            return s
    return None

def find_master_by_credentials(users, username, password):
    for m in users["masters"]:
        if m["name"] == username and m["password"] == password:
            return m
    return None

def student_menu(student):
    while True:
        print(f"=== Student: {student['name']} ({student['id']}) ===")
        print("1) list available courses")
        print("2) request thesis (take course)")
        print("3) view my requests")
        print("4) submit defense request (after 90 days)")
        print("0) logout")
        cmd = input("choice> ").strip()
        users, courses, system = load_all()
        if cmd == "1":
            for c in courses:
                print(f"{c['id']}: {c['title']} - {c['professor_name']} (enrolled {c['enrolled']}/{c['capacity_supervisor']})")
        elif cmd == "2":
            cid = int(input("Enter course id to request: ").strip())
            
            course = next((x for x in courses if x["id"]==cid), None)
            if not course:
                print("course not found")
                continue
            
            req = models.make_request(student['id'], cid)
            system["requests"].append(req)
            save_system(system)
            print("Request submitted. Status: pending")
        elif cmd == "3":
            found = [r for r in system["requests"] if r["student_id"]==student["id"]]
            if not found:
                print("no requests")
            for r in found:
                status = r.get("status")
                print(f"{r['request_id']}: course {r['course_id']} status={status} message={r.get('message','')}")
        elif cmd == "4":
            
            approved = [r for r in system["requests"] if r["student_id"]==student["id"] and r["status"]=="approved"]
            if not approved:
                print("no approved thesis found. can't request defense.")
                continue
            
            import datetime
            req = approved[-1]
            days = (datetime.datetime.now() - datetime.datetime.strptime(req["date"], "%Y-%m-%d")).days
            if days < 90:
                print(f"only {days} days since approval. need 90 days to pass before defense request.")
                continue
            title = input("Enter thesis title: ").strip()
            pdf_path = input("Enter local path to thesis PDF (or leave empty to skip file): ").strip()
            image_path = input("Enter local path to cover image (or leave empty to skip): ").strip()
            files = {}
            if pdf_path:
                try:
                    files["pdf"] = utils.copy_file_to_storage(pdf_path, "pdfs")
                except Exception as e:
                    print("copy pdf failed:", e)
            if image_path:
                try:
                    files["image"] = utils.copy_file_to_storage(image_path, "images")
                except Exception as e:
                    print("copy image failed:", e)
            d = models.make_defense(student["id"], title, files)
            
            d["supervisor_id"] = req.get("supervisor_id")
            system["defenses"].append(d)
            save_system(system)
            print("Defense request submitted.")
        elif cmd == "0":
            break
        else:
            print("unknown choice")

def master_menu(master):
    while True:
        print(f"=== Master: {master['name']} {master['familyname']} ({master['id']}) ===")
        print("1) view pending requests")
        print("2) approve/reject a request")
        print("3) schedule defense (pick date and judges)")
        print("4) view defenses scheduled by me")
        print("0) logout")
        cmd = input("choice> ").strip()
        users, courses, system = load_all()
        if cmd == "1":
            pending = [r for r in system["requests"] if r["status"]=="pending"]
            for r in pending:
                print(f"{r['request_id']}: student {r['student_id']} course {r['course_id']} date {r['date']}")
        elif cmd == "2":
            rid = input("enter request id: ").strip()
            req = next((x for x in system["requests"] if x["request_id"]==rid), None)
            if not req:
                print("request not found")
                continue
            choice = input("approve (a) / reject (r)? ").strip().lower()
            if choice == "a":
        
                
                sup_count = sum(1 for r in system["requests"] if r.get("supervisor_id")==master["id"] and r["status"]=="approved")
                if sup_count >= master.get("capacity_supervisor", 5):
                    print("you have reached supervisor capacity")
                    continue
                req["status"] = "approved"
                req["supervisor_id"] = master["id"]
                req["message"] = "approved by supervisor"
                storage.save("system.json", system)
                print("request approved")
            else:
                req["status"] = "rejected"
                req["message"] = input("enter reason: ").strip()
                storage.save("system.json", system)
                print("request rejected")
        elif cmd == "3":
            
            did = input("enter defense id: ").strip()
            d = next((x for x in system["defenses"] if x["defense_id"]==did), None)
            if not d:
                print("defense not found")
                continue
            date = input("enter scheduled date (YYYY-MM-DD): ").strip()
            internal = int(input("enter internal judge id: ").strip())
            external = int(input("enter external judge id: ").strip())
            
            
            d["scheduled_date"] = date
            d["internal_judge_id"] = internal
            d["external_judge_id"] = external
            
            storage.save("system.json", system)
            print("defense scheduled")
        elif cmd == "4":
            mine = [d for d in system["defenses"] if d.get("supervisor_id")==master["id"]]
            for d in mine:
                print(f"{d['defense_id']}: {d['title']} scheduled {d.get('scheduled_date')}")
        elif cmd == "0":
            break
        else:
            print("unknown choice")

def main():
    print("Thesis Management System (CLI)")
    while True:
        print("1) login as student")
        print("2) login as master")
        print("0) exit")
        choice = input("choice> ").strip()
        users, courses, system = load_all()
        if choice == "1":
            username = input("username (name): ").strip()
            password = input("password: ").strip()
            student = find_student_by_credentials(users, username, password)
            if student:
                student_menu(student)
            else:
                print("invalid credentials")
        elif choice == "2":
            username = input("username (name): ").strip()
            password = input("password: ").strip()
            master = find_master_by_credentials(users, username, password)
            if master:
                master_menu(master)
            else:
                print("invalid credentials")
        elif choice == "0":
            print("bye")
            break
        else:
            print("unknown choice")

if __name__ == "__main__":
    main()