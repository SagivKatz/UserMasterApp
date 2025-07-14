from gmail_utils import authenticate_gmail, scan_inbox

def main():
    service = authenticate_gmail()
    subjects = scan_inbox(service, max_results=10)
    for i, subject in enumerate(subjects, 1):
        print(f"{i}. {subject}")

if __name__ == "__main__":
    main()