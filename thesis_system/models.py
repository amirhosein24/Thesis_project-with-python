from datetime import datetime, timedelta
def make_request(student_id, course_id):
    return {
        "request_id": f"req-{student_id}-{course_id}-{int(datetime.now().timestamp())}",
        "student_id": student_id,
        "course_id": course_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "pending",  
        "supervisor_id": None,
        "message": ""
    }

def make_defense(student_id, thesis_title, files):
    return {
        "defense_id": f"def-{student_id}-{int(datetime.now().timestamp())}",
        "student_id": student_id,
        "title": thesis_title,
        "files": files, 
        "date_requested": datetime.now().strftime("%Y-%m-%d"),
        "scheduled_date": None,
        "supervisor_id": None,
        "internal_judge_id": None,
        "external_judge_id": None,
        "result": None,
        "grades": {}
    }