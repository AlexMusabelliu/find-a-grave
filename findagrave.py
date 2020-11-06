import requests
import pandas as pd
import os, sys
import signal
import time
from bs4 import BeautifulSoup
from votecheck import michigan

def main():
    global cur_point, original_signal
    def save(people):
        print(os.getcwd(), os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "output")))
        if os.getcwd() != os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "output")):
            if not os.path.isdir("output"):
                os.mkdir("output")
            os.chdir("output")

        if not os.path.isfile("confirmed_dead.csv"):
            f = open("confirmed_dead.csv", "w")
            f.write("First Name, Last Name, Birth Year, Matches (here onward)\n")
        else:
            f = open("confirmed_dead.csv", "a")
        # print(first_name, last_name, birth_year, people)
        # print(people)
        matches = ", ".join([p["href"] for p in people[:-1]]) + str(people[-1]["href"])
        # print(matches)
        for i in range(12):
            mo = {0:"January", 1:"February", 2:"March", 3:"April", 
                4:"June", 5:"July", 6:"August", 7:"September", 
                8:"May", 9:"October", 10:"November", 11:"December"}

            re = michigan.get_reg_status(first_name, last_name, mo[i], birth_year, zip_code)

            if re:
                if michigan.is_registered(re):    
                    f.write(f"{first_name},{last_name},{birth_year}," + matches + "\n")
                    break

    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    original_signal = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)
    # signal.pause()

    df = pd.read_csv("MI Dead Voters.csv")

    num_entries = len(df.index)

    starting_point = input("Starting point:    ")

    try:
        starting_point = int(starting_point)
    except:
        print("\nInvalid starting point, using default = 0 (all data)\n\n")
        starting_point = 0

    location = "Detroit,+Michigan"
    filter_type = "exact"

    death_year = dfilter_type = middle_name = ""

    for cur_point in range(starting_point, num_entries):
        row = df.iloc[cur_point].T
        # print(row)
        # print(row[1], row[2], row[3])
        first_name = row[1]
        last_name = row[2]
        birth_year = row[3]
        zip_code = row[4]

        result = requests.get(f"https://www.findagrave.com/memorial/search?"\
            f"firstname={first_name}"\
            f"&middlename={middle_name}"\
            f"&lastname={last_name}"\
            f"&birthyear={birth_year}&"\
            f"birthyearfilter={filter_type}"\
            f"&deathyear={death_year}"\
            f"&deathyearfilter={dfilter_type}"\
            f"&location={location}"\
            f"&locationId="\
            f"&memorialid="\
            f"&mcid="\
            f"&linkedToName="\
            f"&datefilter="\
            f"&orderby=")

        data = BeautifulSoup(result.content, "html.parser")
        dead_persons = data.find_all("a", attrs={"class":"memorial-item"})
        # print(dead_persons)
        if dead_persons != []:
            save(dead_persons)

def signal_handler(sig, frame):
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    signal.signal(signal.SIGINT, original_signal)
    nun = time.strftime("%x")
    with open(f"log{nun}.txt", "w") as f:
        f.write(f"stopped at: {cur_point}")
    sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main()