from colorama import Fore, init

init(autoreset=True)        #  note: this is optional (this can add colors to your terminal lines)   




# function that will find us the total entries in sample.log 
def total_lines():
    with open("sample.log", "r") as  file_lines:
        entries = file_lines.readlines()


    return entries

entrieslines = total_lines()


# functions to get succesful anf failed logins attempts
successful_attempts = []
failed_attempts = []



for lines in total_lines():
    if "Login successful" in lines:
        successful_attempts.append(lines)

    elif "Login failed" in lines:
        failed_attempts.append(lines)    

# getting total no of users that signed in and logged out 
signed_in = []
signed_out = []

for line_in in total_lines():
    if "Signed In" in line_in:
        signed_in.append(line_in)

for line_out in total_lines():
    if  "Logout" in line_out:
        signed_out.append(line_out)        

# gettig ips of login that were failed

failed_login_ips = []

for line in failed_attempts:
    p = line.split()
    ip = p[-1].replace("ip=", "")
    failed_login_ips.append(ip)

print(f"Total entries found : {len(entrieslines)}")
print("\n")
print(Fore.GREEN + f"Total succesful logins : {len(successful_attempts)}")
print(Fore.RED + f"Total failed logins : {len(failed_attempts)}")


print(f"Total signed in users : {len(signed_in)}")
print(f"Total signed out users : {len(signed_out)}")



# loop for failed ip
print("\nSuspicious IP detection:")

for ip in set(failed_login_ips):
    attempt_count = failed_login_ips.count(ip)

    if attempt_count >= 3:
        print(
            Fore.RED
            + f"WARNING!!! Suspicious IP detected: {ip} | Failed attempts: {attempt_count}"
        )

        print("Failed login entries from this IP:")

        for line in failed_attempts:
            if ip in line:
                print(line.strip())








# report saving        


save_report = input("Do you wanna save this report in a file? yes or no : ")


if save_report.lower() == "yes":
    with open("security_report.txt", "w") as report:
        report.write("LogSentinel Security Report\n")
        report.write("===========================\n")
        report.write(f"Total entries found: {len(entrieslines)}\n")
        report.write(f"Successful logins: {len(successful_attempts)}\n")
        report.write(f"Failed logins: {len(failed_attempts)}\n")
        report.write(f"Signed in entries: {len(signed_in)}\n")
        report.write(f"Signed out entries: {len(signed_out)}\n")

    print(Fore.GREEN + "Report saved to report_log_analyzer.txt")

else:
    print("Report was not saved, as you pressed no!")