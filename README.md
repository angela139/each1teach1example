# Each1Teach1 Leaderboard
#### This is a website that I have created for the program Each1Teach1 to monitor interns' scores. It uses the Google Classroom API to get grades from the interns' work. It is currently being hosted on Heroku on this [website]("https://e1t1-leaderboard.herokuapp.com/").

# Using the leaderboard for your own students on local computer
1. Fork this project and clone to local computer.
2. Install Google client library for Python <br>
`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
3. Create a Google Cloud Platform project with the Google Classroom API enabled.
4. Create credentials for a desktop app for the project on the Google Cloud Console.
5. Download the credentials.json file to your local computer and add it to the project directory. 
6. Comment out the following code <br>
    `else:
        creds = Credentials.from_authorized_user_info(
            {"token": os.environ['TOKEN'],
             "refresh_token": os.environ['REFRESH_TOKEN'],
             "token_uri": os.environ['TOKEN_URI'],
             "client_id": os.environ['CLIENT_ID'],
             "client_secret": os.environ['CLIENT_SECRET'],
             "scopes": SCOPES,
             "expiry": os.environ['EXPIRY']})`

7. Uncomment the following code <br>
    `if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())`

8. Run leaderboard.py which will prompt you to authorize the request.
9. A token.json file should be made to authorize future API requests.
10. Adjust code in leaderboard.py for your classroom. 
11. Run app.py to see your leaderboard! 