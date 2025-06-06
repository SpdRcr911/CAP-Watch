import os
import requests
import sys
import base64
import zipfile

def download_and_extract_capwatch(org, file_path, unit_only=0):
    if not org:
        raise ValueError("A value for 'org' must be supplied.")
    if not file_path:
        raise ValueError("A value for 'file_path' must be supplied.")
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
        extract_dir = os.path.dirname(os.path.abspath(file_path))
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        for fname in os.listdir(extract_dir):
            if fname.lower().endswith('.pdf'):
                os.remove(os.path.join(extract_dir, fname))
            elif fname.lower().endswith('.txt'):
                base = os.path.splitext(fname)[0]
                new_name = base + '.csv'
                os.rename(os.path.join(extract_dir, fname), os.path.join(extract_dir, new_name))
    else:
        raise Exception(f"Failed to fetch data: {response.status_code} {response.reason}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python download_and_extract_capwatch.py <org> <file_path> [unit_only]")
        sys.exit(1)
    org = sys.argv[1]
    file_path = sys.argv[2]
    unit_only = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    try:
        download_and_extract_capwatch(org, file_path, unit_only)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
