from colorama import Fore, init

init(autoreset=True)        #  note: this is optional (this can add colors to your terminal lines)   




# function that will find us the total entries in sample.log 
def total_lines():
    with open("sample.log", "r") as  file_lines:
        entries = file_lines.readlines()


        return entries



entrieslines = total_lines()
print(f"Total entries found : {len(entrieslines)}")