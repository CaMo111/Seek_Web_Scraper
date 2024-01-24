from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

what_input = str(input("Job Search Query: "))
where_input = str(input("Job Location: "))

def search(what_input, where_input):
    url = f"https://www.seek.com.au/{what_input}-jobs/in-{where_input}"
    print(url)
    req = requests.get(url)
    data = req.text
    soup = BeautifulSoup(data, "html.parser")
    data_collation = soup.find_all("div", {"class": "_1wkzzau0 a1msqi6m"}, limit=800)
    count = 1

    '''
    We should collect the following information;
    jobTitle
    jobCompany
    jobListingDate
    jobLocation
    jobShortDescrption
    jobClassification
    job-list-view-job-link
    '''

    cols = ["jobTitle","jobCompany", "jobListingDate", "jobLocation", "jobClassification", "jobSalary"]

    def extract_jobInformation(job_listing, coltype):
        elem = job_listing.find(attrs={"data-automation": coltype})
        try:
            outcome = elem.text.strip()
        except:
            outcome = None
        return outcome

    res = {}

    def collate_data():
        for data in cols:
            try:
                test = res[data]
            except:
                res[data] = []

            for idx, job_elem in enumerate(data_collation):
                outcome = extract_jobInformation(job_elem, data)
                if outcome != None:
                    res[data].append(outcome)
                    #res.append(outcome)
                else:
                    res[data].append("NA")

    def save_jobs_to_excel(data, filename):
        jobs = pd.DataFrame(data)
        jobs.to_csv(filename)

    for i in range(25):
        if count == 1:
            collate_data()
            count += 1 
        else:
            print("called")
            url = f'https://www.seek.com.au/{what_input}/{where_input}' + f'?page={count}'
            req = requests.get(url)
            data = req.text
            soup = BeautifulSoup(data, "html.parser")
            data_collation = soup.find_all("div", {"class": "_1wkzzau0 a1msqi6m"}, limit=800)
            collate_data()
            count += 1 
            print(count)

    #This somehow cleanses the job location data
    def cleanse():
        for i in range(len(res['jobLocation'])):
            try:
                res['jobLocation'].pop(i)
            except:
                break

    res2 = []

    def output():
        #this should be more of a writing to JSON file
        cleanse()
        for nums in (range(25000)):
            print("\n")
            try:
                print(nums)
                print(f"The position of {res[cols[0]][nums]} is being offered by {res[cols[1]][nums]}. The listing was put up {res[cols[2]][nums]} days ago. It is based in {res[cols[3]][nums]} and is subclassified by: {res[cols[4]][nums]}. {res[cols[5]][nums]}")
            except:
                break
            print("\n")

    for nums in (range(2500)):
        try:
            res2.append([res[cols[0]][nums], res[cols[1]][nums], res[cols[2]][nums], res[cols[3]][nums], res[cols[4]][nums], res[cols[5]][nums]])
        except:
            break

    res3 = []

    for items in res2:
        if "NA" not in items[:4]:
            res3.append(items)

    for items in res3:
        print("\n")
        print(f"The position of {items[0]} is being offered by {items[1]}. The listing was put up {items[2]}. It is based in {items[3]} and is subclassified by: {items[4]}. Salary:{items[5]}")

search(what_input, where_input)