from colorama import Fore, init

init(autoreset=True)        #  note: this is optional (this can add colors to your terminal lines)   




# function that will find us the total entries in sample.log 
def total_lines():
    with open("sample.log", "r") as  file_lines:
        entries = file_lines.readlines()


    return entries



# functions to get succesful anf failed logins attempts
successful_attempts = []
failed_attempts = []


for lines in total_lines():
    if "Login successful" in lines:
        successful_attempts.append(lines)

    elif "Login failed" in lines:
        failed_attempts.append(lines)    



entrieslines = total_lines()


print(f"Total entries found : {len(entrieslines)}")
print("\n")
print(Fore.GREEN + f"Total succesful logins : {len(successful_attempts)}")
print(Fore.RED + f"Total failed logins : {len(failed_attempts)}")


