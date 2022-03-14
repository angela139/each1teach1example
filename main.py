from __future__ import print_function
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students',
          'https://www.googleapis.com/auth/classroom.rosters', 'https://www.googleapis.com/auth/classroom.courses']

coursework_array = []
student_work_array = []
student_array = []
course_id_array = []


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
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

    service = build('classroom', 'v1', credentials=creds)
    # Get courses
    courses = service.courses().list().execute()
    for course in courses["courses"]:
        if "E1T1" in course["name"]:
            course_id_array.append(course["id"])

    for id in course_id_array:
        # Get students unique ids
        students = service.courses().students().list(courseId=id).execute()
        for student in students["students"]:
            student_dict = {"id": student["userId"], "name": student["profile"]["name"]["givenName"]}
            student_array.append(student_dict)

    print(student_array)


if __name__ == '__main__':
    main()
