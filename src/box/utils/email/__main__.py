from box.utils.email.utils import send_email


def main() -> None:
    send_email("test@test.com", "Test", "Test")


if __name__ == "__main__":
    main()
