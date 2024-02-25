from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import subprocess
import re
import time
import pandas as pd

from .utils import *

output_fileids = {}

# def handle_termination(signum, frame):
#     print("Killing all test servers")

class TestServer:
    count=0
    def __init__(self):
        
        self.init_filename = f"init_{TestServer.count}"
        self.latter_filename = f"latter_{TestServer.count}"

        with open("./output/"+self.init_filename, "w") as f:
            f.write("")
        with open("./output/"+self.latter_filename, "w") as f:
            f.write("")

        command = f"(./interactsh-client | tee ./output/{self.latter_filename}) 3>&1 1>&2 2>&3 | tee ./output/{self.init_filename}"
        self.server = subprocess.Popen(command, shell=True, text=True)
        pattern = re.compile(r'.*oast.*')
        time.sleep(5)
        with open("./output/"+self.init_filename, 'r') as f:
            text = f.read()
            print(text)
            self.url = pattern.findall(text)[0].split()[1]

        print(TestServer.count)
        TestServer.count+=1

    def get_url(self):
        return self.url


@api_view(['GET'])
def get_url(request):

    server = TestServer()
    output_fileids[server.url] = TestServer.count-1
    print(output_fileids)
    
    url = server.get_url()
    return Response({"url": url}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_interactions(request):
    print(request.data)
    file_id = output_fileids[request.data['url']]

    with open(f'./output/latter_{file_id}', 'r') as f:
        interactions = f.readlines()

    interactions = [parse_interaction(interaction) for interaction in interactions]
    interactions = pd.DataFrame(interactions)

    interactions['timestamp'] = pd.to_datetime(interactions['timestamp'])
    from_timestamp = pd.to_datetime(request.data.get("from_timestamp", None))
    to_timestamp = pd.to_datetime(request.data.get("to_timestamp", None))

    
    if from_timestamp is not None: interactions = interactions[(interactions['timestamp'] >= from_timestamp)]
    if to_timestamp is not None: interactions = interactions[(interactions['timestamp'] <= to_timestamp)]
    print(interactions)
    return Response({'interactions': interactions.to_dict("index")}, status=status.HTTP_200_OK)