from pythonbridge.config import load_environment


def main():
    # Load the environment variables
    load_environment()

    # Here, we probably want to call the python bridge
    print("Hello from python!")


if __name__ == "__main__":
    main()
