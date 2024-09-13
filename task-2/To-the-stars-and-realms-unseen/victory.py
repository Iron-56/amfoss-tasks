import sys
import subprocess

def get_git_username():
    try:
        result = subprocess.run(['git', 'config', '--global', 'user.name'], capture_output=True, text=True, check=True)
        username = result.stdout.strip()
        return username
    except subprocess.CalledProcessError:
        return None

def display_victory_message(username):
    if username:
        message = (
            f"Congratulations {username}!!! You have successfully overcome the challenges and escaped the deadly clutches of Arrakis-dex.\n"
            "You will now be able to join the war again spreading your faith for the Emperor and humankind!!\n"
            "Take a screenshot of this and save it in your handbook folder along with the other codes you have collected.\n"
            "Stand proud, champion!"
        )
        print(message)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != '--run':
        print("This script must be run with the '--run' argument from the command line.")
        sys.exit(1)


    display_victory_message("BlackKitty")
