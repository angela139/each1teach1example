from __future__ import print_function
import app_auth
from googleapiclient.discovery import build
from firebase_admin import db
from dotenv import load_dotenv
load_dotenv()


def get_scores():
    coursework_array = []
    student_array = []
    course_id = ""

    service = build('classroom', 'v1',
                    credentials=app_auth.connect_google_classroom())
    course_list = service.courses()

    # Get courses
    courses = course_list.list().execute()
    for course in courses["courses"]:
        if "E1T1 Spring" in course["name"]:
            course_id = course["id"]

    # Get students
    students = service.courses().students().list(courseId=course_id).execute()
    for student in students["students"]:
        student_dict = {"id": student["userId"], "name": student["profile"]["name"]["givenName"], "score": 0}
        student_array.append(student_dict)

    # Get all courseWork
    assignments = course_list.courseWork().list(courseId=course_id).execute()
    for assignment in assignments["courseWork"]:
        coursework_array.append(assignment["id"])

    # Get students scores from work
    for coursework in coursework_array:
        grades = course_list.courseWork().studentSubmissions().list(courseId=course_id,
                                                                    courseWorkId=coursework).execute()
        for grade in grades["studentSubmissions"]:
            try:
                for intern in student_array:
                    if intern["id"] == grade["userId"]:
                        intern["score"] += int(grade["assignedGrade"])
            except:
                pass

    return student_array


def update_scores(student_array):
    app_auth.connect_firebase()
    ref = db.reference('/interns')
    current_scores = ref.get()
    for key, value in current_scores.items():
        for intern in student_array:
            if value["name"] == intern["name"]:
                if value["score"] != intern["score"]:
                    ref.child(key).update({"score": f'{intern["score"]}'})
                else:
                    pass
            else:
                pass


# def add_intern() "Function to handle new node/user"

def main():
    new_stats = get_scores()
    update_scores(new_stats)


if __name__ == "__main__":
    main()
