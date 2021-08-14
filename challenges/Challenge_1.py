import os
import time
#Dependencies
from azure.cognitiveservices.knowledge.qnamaker.authoring import QnAMakerClient
from azure.cognitiveservices.knowledge.qnamaker.runtime import QnAMakerRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from utils.kb_helper import create_kb, download_kb, publish_kb, getEndpointKeys_kb
from utils.kb_helper import generate_answer, _monitor_operation

#Key and endpoint
subscription_key = '<subscription key>'

authoring_endpoint = '<authoring endpoint from Azure>'

runtime_endpoint = '<runtime endpoint from Azure>'

#Instantiate client application

client = QnAMakerClient(endpoint=authoring_endpoint, 
                        credentials=CognitiveServicesCredentials(subscription_key))
kb_id = create_kb(client=client)
#TODO: Update KB function
publish_kb(client=client, kb_id=kb_id)
download_kb(client=client, kb_id=kb_id)
queryRuntimeKey = getEndpointKeys_kb(client=client)
#Authenticate runtime from client application
runtimeClient = QnAMakerRuntimeClient(runtime_endpoint=runtime_endpoint, 
                                      credentials=CognitiveServicesCredentials(queryRuntimeKey))
generate_answer(client=runtimeClient,kb_id=kb_id,
                runtimeKey=queryRuntimeKey)
