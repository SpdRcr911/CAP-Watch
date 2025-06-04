import os
import requests
import sys
import base64

def invoke_cap_watch(org, file_path, unit_only=0):
    if not org:
        raise ValueError("A value for 'org' must be supplied.")

    if not file_path:
        raise ValueError("A value for 'file_path' must be supplied.")

    # Retrieve username and password from environment variables
    user = os.getenv('CAP_USERNAME')
    user_pass = os.getenv('CAP_PASSWORD')

    if not user or not user_pass:
        raise EnvironmentError("Environment variables CAP_USERNAME and CAP_PASSWORD must be set.")

    pair = f"{user}:{user_pass}"
    base64_bytes = base64.b64encode(pair.encode('ascii'))
    base64_pair = base64_bytes.decode('ascii')

    headers = {
        'Authorization': f'Basic {base64_pair}'
    }

    url = f"https://www.capnhq.gov/CAP.CapWatchAPI.Web/api/cw?ORGID={org}&unitOnly={unit_only}"

    response = requests.get(url, headers=headers, timeout=600)

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Failed to fetch data: {response.status_code} {response.reason}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python invokeCapWatch.py <org> <file_path> [unit_only]")
        sys.exit(1)

    org = sys.argv[1]
    file_path = sys.argv[2]
    unit_only = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    try:
        invoke_cap_watch(org, file_path, unit_only)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)