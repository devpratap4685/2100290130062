import requests
from flask import Flask, jsonify

app = Flask(__name__)

window_size = 10
window = []

def fetch_numbers(qualifier, token):
    headers = {"Authorization": f"Bearer {token}"}
    if qualifier == 'p':
        response = requests.get("http://20.244.56.144/test/primes", headers=headers)
    elif qualifier == 'f':
        response = requests.get("http://20.244.56.144/test/fibo", headers=headers)
    elif qualifier == 'e':
        response = requests.get("http://20.244.56.144/test/even", headers=headers)
    elif qualifier == 'r':
        response = requests.get("http://20.244.56.144/test/rand", headers=headers)
    else:
        return None
    return response.json()["numbers"]

def update_window(new_numbers):
    global window
    window += new_numbers
    window = list(set(window))  # Ensure uniqueness
    if len(window) > window_size:
        window = window[-window_size:]

@app.route('/numbers/<qualifier>')
def calculate_average(qualifier):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE3MjI1NjYyLCJpYXQiOjE3MTcyMjUzNjIsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjY0MjZiMGMwLTE0OWItNDIyMS04NWE1LWI5M2Y1YzIzMTk0MiIsInN1YiI6ImRldjIxMjVpdDEwODdAa2lldC5lZHV1In0sImNvbXBhbnlOYW1lIjoiTmV3IFRlY2giLCJjbGllbnRJRCI6IjY0MjZiMGMwLTE0OWItNDIyMS04NWE1LWI5M2Y1YzIzMTk0MiIsImNsaWVudFNlY3JldCI6InN4WmtndHNER0xmcm5iSEEiLCJvd25lck5hbWUiOiJEZXYgUHJhdGFwIFNpbmdoIiwib3duZXJFbWFpbCI6ImRldjIxMjVpdDEwODdAa2lldC5lZHV1Iiwicm9sbE5vIjoiMjEwMDI5MDEzMDA2MiJ9.UYzE3U42Dlw38_8tJrGB8c8cWlljRV2IqW9LlvuyjFo"  # Replace this with your actual bearer token
    numbers = fetch_numbers(qualifier, token)
    if numbers is None:
        return jsonify({"error": "Invalid qualifier"}), 400
    
    window_prev_state = window[:]
    update_window(numbers)
    window_curr_state = window[:]
    
    average = sum(window) / len(window) if window else 0
    
    response = {
        "numbers": numbers,
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "avg": average
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
