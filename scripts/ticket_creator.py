## THIS CODE CREATES NEW TICKETS AND PRINTS OUT THEIR RESPECTIVE ID IN THE TERMINAL

from base64 import b64encode
import configparser
import requests
import json
import time

config = configparser.RawConfigParser()
config.read('./src/auth.ini')
DOMAIN = config['zendesk']['Domain'].strip('"')
AUTH = config['zendesk']['Credentials'].strip('"')

def main():
    create_ticket()

def create_ticket():
    i = 0
    tickets_to_be_created = 100 ## INPUT HOW MANY TICKETS YOU WANT TO CREATE
    t = tickets_to_be_created
    json_data = []
    dat = {"tickets": json_data}
    while i < t: 
        content = {"subject": "API CREATED TICKET " + str(i + 101), 
                        "comment": { "body": "This ticket has been created via an API request. Ticket #" + str(i + 101)}}
        json_data.append(content)
        i = i + 1

    url = 'https://{}.zendesk.com/api/v2/tickets/create_many.json'.format(DOMAIN)
    header = {"Authorization": "Basic {}".format(str(b64encode(AUTH.encode('utf-8')))[2:-1]), 'Content-type': 'application/json'}
    
    try:
        result = requests.post(url, data=json.dumps(dat), headers=header)
        result = json.loads(result.text)
        jobstatus_url = result["job_status"]["url"]
        print("Follow this link for the job status: " + jobstatus_url)
        jobstatus = requests.get(jobstatus_url, headers=header)
        jobstatus = json.loads(jobstatus.text)
        while jobstatus["job_status"]["status"] != "completed":
            print("Refreshing: 15 second wait time...")
            time.sleep(15)
            jobstatus = requests.get(jobstatus_url, headers=header)
            jobstatus = json.loads(jobstatus.text)
        else:
            n = 0
            print("Please see the ticket IDs below:")
            while n < t:
                print(jobstatus["job_status"]["results"][n]["id"])
                n = n + 1

        # time.sleep(10)
        # jobstatus = requests.get(jobstatus_url, headers=header)
        # jobstatus = json.loads(jobstatus.text)
        # ticket_id = jobstatus["job_status"]["results"][0]["id"]
        # print(ticket_id) ## Will print out the ticket numbers, easy for copy-pasting into a spreadsheet or csv
    except Exception as e:
        print('Error: ', str(e))
        exit()

if __name__ =="__main__":
    main()