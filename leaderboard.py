from __future__ import print_function
import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def get_scores():
    SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students',
              'https://www.googleapis.com/auth/classroom.rosters', 'https://www.googleapis.com/auth/classroom.courses']
    coursework_array = []
    student_array = []
    course_id = ""

    # Authorize user for Google Classroom API
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file("token.json")
    else:
        creds = Credentials.from_authorized_user_info(
            {"token": os.environ['TOKEN'],
             "refresh_token": os.environ['REFRESH_TOKEN'],
             "token_uri": os.environ['TOKEN_URI'],
             "client_id": os.environ['CLIENT_ID'],
             "client_secret": os.environ['CLIENT_SECRET'],
             "scopes": SCOPES,
             "expiry": os.environ['EXPIRY']})
    '''
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    '''

    service = build('classroom', 'v1', credentials=creds)
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
