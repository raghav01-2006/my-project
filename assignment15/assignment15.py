import sys
import datetime

def main():
    print("=" * 50)
    print("Dockerized Python Application (Assignment 15)")
    print("=" * 50)
    print(f"Current Python Version: {sys.version}")
    print(f"Current Date and Time:  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

if __name__ == "__main__":
    main()
