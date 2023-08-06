import requests
import webbrowser

def get_secure_1psid():
    """Gets the value of the __Secure-1PSID cookie from the browser."""
    url = "https://bard.google.com/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to get __Secure-1PSID cookie.")

    secure_1psid = response.cookies.get("__Secure-1PSID")
    if not secure_1psid:
        raise Exception("__Secure-1PSID cookie not found.")

    return secure_1psid

def parse_secure_1psid(value):
    """Parses the __Secure-1PSID cookie."""
    parsed_cookie = {}
    for pair in value.split(";"):
        key, value = pair.split("=", 1)
        parsed_cookie[key] = value
    return parsed_cookie

def main():
    """Gets the __Secure-1PSID cookie directly from the browser and prints it out."""
    secure_1psid = get_secure_1psid()
    parsed_secure_1psid = parse_secure_1psid(secure_1psid)
    print(parsed_secure_1psid)

if __name__ == "__main__":
    main()
