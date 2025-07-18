import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyODIzODM4LCJpYXQiOjE3NTI4MjM1MzgsImp0aSI6IjJjMTMzYTFlZTQ2ZjQ4YjI4M2NmZDljN2IwNDk0MzJhIiwidXNlcl9pZCI6MywiZnVsbF9uYW1lIjoiS2FucmFuIiwiZW1haWwiOiJrYW1yYW5AZ21haWwuY29tIiwidXNlcm5hbWUiOiJrYW1yYW4ifQ.oxlaUA3WKYMWbl_RTHLThrenMvaLPrIf8QdKlJBsC5Q" 
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get("http://127.0.0.1:8000/api/v1/my-bookings/", headers=headers)
print(response.json())