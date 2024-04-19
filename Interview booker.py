# Interview booker

from google.oauth2 import service_account
import googleapiclient.discovery

# Load credentials from service account file
credentials = service_account.Credentials.from_service_account_file(
    '/path/to/service-account-file.json',
    scopes=['https://www.googleapis.com/auth/calendar']
)

def schedule_meeting(candidate_name, meeting_time):
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    event = {
        'summary': f'Interview with {candidate_name}',
        'start': {
            'dateTime': meeting_time,  # Format: 'YYYY-MM-DDTHH:MM:SS'
            'timeZone': 'Your Timezone',
        },
        'end': {
            'dateTime': meeting_time,  # Adjust the end time as needed
            'timeZone': 'Your Timezone',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'random-string-id',
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
            },
        },
    }
    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    meeting_link = event.get('hangoutLink')
    return meeting_link

# Example usage
def book_interview(candidate_name, meeting_time):
    meeting_link = schedule_meeting(candidate_name, meeting_time)
    print(f"Interview scheduled with {candidate_name}. Meeting link: {meeting_link}")

# Test Run
top_candidates = ranked_candidates[:5]
for candidate_info, score in top_candidates:
    candidate_name = candidate_info.split('\n')[0]
    meeting_time = '2024-04-20T10:00:00'  # Example meeting time (adjust as needed)
    book_interview(candidate_name, meeting_time)
