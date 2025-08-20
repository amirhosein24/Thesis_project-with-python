# Thesis Management System (Python CLI)

##  Overview  
This is a **Command-Line Interface (CLI)** project for managing university thesis processes.  
It allows **students** to request thesis courses and submit defense requests, and **masters** (professors) to approve/reject requests and schedule defenses.  

The project uses:  
- **Python** 
- **JSON**   
- **PDF / JPG** (for storing thesis files)  
- **Command-Line Interface**  

---

##  Features  

### Student  
- **Login** with student ID and password  
- View available thesis courses  
- Request to take a thesis course (capacity checked)  
- View the status of requests: `pending`, `approved`, `rejected`  
- Re-submit if rejected  
- Submit defense request (after 90 days of approval)  
- Upload final thesis files (PDF, cover image)  
- Search in defended thesis archive  

### Master (Professor)  
- **Login** with master ID and password  
- View and approve/reject student thesis requests  
- Schedule defense date and assign judges (1 internal, 1 external)  
- Approve final thesis before defense  
- Record defense results and grades  

##  How to Run  

1. Make sure you have **Python 3** installed.  
2. Open a terminal in the project folder.  
3. Run:
   python3 main.py
Login as a student or master using the credentials in users.json.
