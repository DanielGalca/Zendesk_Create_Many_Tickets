## THIS CODE CREATES NEW TICKETS AND PRINTS OUT THEIR RESPECTIVE ID IN THE TERMINAL

from base64 import b64encode
import configparser
import json
import time
import requests

config = configparser.RawConfigParser()
config.read('./src/auth.ini')
DOMAIN = config['zendesk']['Domain'].strip('"')
AUTH = config['zendesk']['Credentials'].strip('"')

def main():
    create_ticket()

def create_ticket():
    i = 0
    tickets_to_be_created = 368 ## INPUT HOW MANY TICKETS YOU WANT TO CREATE
    url = 'https://{}.zendesk.com/api/v2/tickets/create_many.json'.format(DOMAIN)
    header = {"Authorization": "Basic {}".format(str(b64encode(AUTH.encode('utf-8')))[2:-1]), 'Content-type': 'application/json'}
    id_list = []
    json_data = []
    dat = {"tickets": json_data}
    while i < tickets_to_be_created:
        content = {"subject": "DO NOT OPEN " + str(i + 1),
                        "comment": { "body": "This ticket has been created via an API request. Ticket #" + str(i + 1)}}
        json_data.append(content)
        if i % 100 == 99 or i == tickets_to_be_created - 1:
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
                k = 0
                while k < len(json_data):
                    id_list.append(jobstatus["job_status"]["results"][k]["id"])
                    k = k + 1
                json_data.clear()
            except Exception as err_msg:
                print('Error creating tickets: ', str(err_msg))
        i = i + 1
    print("Tickets created: " + len(id_list))

if __name__ =="__main__":
    main()
