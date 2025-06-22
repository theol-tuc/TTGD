import requests

BASE_URL = 'http://localhost:8000'

# Endpoints to test (method, path, payload)
endpoints = [
    ('GET', '/', None),
    ('GET', '/board', None),
    ('POST', '/set-board', {'board': [['.' for _ in range(15)] for _ in range(17)]}),
    ('POST', '/components', {'type': 'RAMP_LEFT', 'x': 1, 'y': 1}),
    ('POST', '/marbles', {'color': 'blue'}),
    ('GET', '/output', None),
    ('POST', '/launcher', {'launcher': 'left'}),
    ('POST', '/update', None),
    ('POST', '/reset', None),
    ('GET', '/counts', None),
    ('GET', '/challenge_id', {'challenge_id': 'challenge_01'}),
    ('POST', '/ai/move', {}),
    ('POST', '/ai/execute', {}),
    ('POST', '/drop-marble', {'board': [['.' for _ in range(15)] for _ in range(17)], 'side': 'left'}),
    ('POST', '/reset-board', None),
    ('POST', '/solve', {'components': [], 'marble_color': 'blue'}),
]

def test_endpoint(method, path, payload=None):
    url = BASE_URL + path
    try:
        if method == 'GET':
            if payload:
                resp = requests.get(url, params=payload)
            else:
                resp = requests.get(url)
        elif method == 'POST':
            resp = requests.post(url, json=payload) if payload is not None else requests.post(url)
        else:
            print(f"Unsupported method: {method}")
            return
        print(f"{method} {path} -> Status: {resp.status_code}")
        try:
            print("  Response:", resp.json())
        except Exception:
            print("  Response (non-JSON):", resp.text)
    except Exception as e:
        print(f"{method} {path} -> ERROR: {e}")

if __name__ == '__main__':
    for method, path, payload in endpoints:
        test_endpoint(method, path, payload)
        print('-' * 60) 