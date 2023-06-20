#!/usr/bin/env python3
from edgegrid.edgegrid import EdgeGridAuth
from urllib.parse import urljoin
import requests
import os
from datetime import datetime

apipath = "/siteshield/v1/maps/4829"
apistagingpath = "/firewall-rules-manager/v1/cidr-blocks"

def make_session(): 
    content = []
    filename = f"{os.path.dirname(os.path.abspath(__file__))}/apiclient.txt"
    with open(filename, "r", encoding='utf_8') as file:
        for line in file:
            content.append(line.strip("\n"))
    cl_secret = content[0]
    burl = content[1]
    acc_token = content[2]
    cl_token = content[3]
    session = requests.Session()
    session.auth = EdgeGridAuth(
        client_token = cl_token,
        client_secret = cl_secret,
        access_token = acc_token,
    )
    return session, burl

def write_output(data:tuple):
    filenames = ("siteshield.txt", "siteshield_staging.txt", "siteshield_staging_v6.txt", "siteshieldv6.txt" )
    for i, iplist in enumerate(data):
        filepath = f"{os.path.dirname(os.path.abspath(__file__))}/{filenames[i]}"
        f = open(filepath, "w", encoding="utf-8")
        for item in iplist:
            #newline at the end of file is intentional
            f.write(f"{item}\n")
        f.close()

def log_response(r: requests.Response):
    with open ("log.txt", "a", encoding="utf-8") as f:
        try:
            f.write(f"timestamp: {datetime.now().strftime('%d-%m-%y %H:%M:%S')};\n code: {r.status_code};\n headers: {r.headers};\n body:{r.json()}\n\n")
        except ValueError:
            f.write(f"Something broke :(")

def get_data(s: requests.Session, burl: str):
    headers = {"accept": "application/json"}
    url = urljoin(burl, apipath)
    r = s.get(url, headers=headers)
    if r.status_code == 200:
        current = r.json()["currentCidrs"]
        proposed = r.json()["proposedCidrs"]
        ssprod = list(set(current) | set (proposed))
        #we might have to make an ipv6 version variable in the future
        #ssv6prod = ???
    log_response(r)

    url = urljoin(burl, apistagingpath)
    r = s.get(url, headers=headers)
    if r.status_code == 200:
        ssstage = []
        ssv6stage = []
        for item in r.json():
            cidr = f"{item['cidr']}{item['cidrMask']}"
            if ":" in cidr:
                ssv6stage.append(cidr)
            else:
                ssstage.append(cidr)
    log_response(r)
    #if ipv6 gets introduced into siteshield, I'll need to return another var at the end of tuple
    return (ssprod, ssstage, ssv6stage) 

def main():
    ses, burl = make_session()
    print("Fetching siteshield data...")
    data = get_data(ses, burl)
    print("Writing data into respective files...")
    write_output(data)

if __name__ == "__main__":
    main()
