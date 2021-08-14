import os
import time

#Dependencies
from azure.cognitiveservices.knowledge.qnamaker.authoring.models import QnADTO, MetadataDTO, CreateKbDTO, OperationStateType, UpdateKbOperationDTO, UpdateKbOperationDTOAdd, EndpointKeysDTO, QnADTOContext, PromptDTO
from azure.cognitiveservices.knowledge.qnamaker.runtime.models import QueryDTO

#Get status of operation
def _monitor_operation(client, operation):

    for i in range(20):
        if operation.operation_state in [OperationStateType.not_started, OperationStateType.running]:
            print("Waiting for operation: {} to complete.".format(operation.operation_id))
            time.sleep(5)
            operation = client.operations.get_details(operation_id=operation.operation_id)
        else:
            break
    if operation.operation_state != OperationStateType.succeeded:
        raise Exception("Operation {} failed to complete.".format(operation.operation_id))

    return operation

#Define and create KB
def create_kb(client):
    print ("Creating knowledge base...")

    qna1 = QnADTO(
        answer="You can cancel a flight or hotel anytime up to 24 hours before check-in. A cancellation fee may apply. Call us on 555 123 456; or visit our website: www.margiestravel.com",
        questions=["How can I cancel my hotel reservation?"],
        metadata=[
            MetadataDTO(name="Category", value="api"),
            MetadataDTO(name="Language", value="Python"),
        ]
    )

    qna2 = QnADTO(
        answer="Margie’s Travel is a full-service travel agent, with years of experience in the worldwide tourism industry.",
        questions=["What is Margie's Travel?"],
        metadata=[
            MetadataDTO(name="Category", value="api"),
            MetadataDTO(name="Language", value="Python"),
        ]
    )

    qna3 = QnADTO(
        answer="Margie’s Travel can help arrange flights, accommodation, airport transfers, excursions, visas, travel insurance, and currency exchange.",
        questions=["What services are provided?"],
        metadata=[
            MetadataDTO(name="Category", value="api"),
            MetadataDTO(name="Language", value="Python"),
        ]
    )

    qna4 = QnADTO(
    answer="We can arrange travel anywhere in the world, but we specialize in trips to Dubai, Las Vegas, London, New York, and San Francisco.",
    questions=["Where can I travel to?"],
    metadata=[
        MetadataDTO(name="Category", value="api"),
        MetadataDTO(name="Language", value="Python"),
        ]
    )

    qna5 = QnADTO(
    answer="Our agents can help you book flights between any major airports, on any of the major airlines. We offer competitive fares for all flight classes. To book a flight, call us on 555 123 456; or visit our website: www.margiestravel.com.",
    questions=["How can I book a flight?"],
    metadata=[
        MetadataDTO(name="Category", value="api"),
        MetadataDTO(name="Language", value="Python"),
        ]
    )

    qna5 = QnADTO(
    answer="Call us on 555 123 456; or visit our website: www.margiestravel.com.",
    questions=["How can contact Margie's Travel?"],
    metadata=[
        MetadataDTO(name="Category", value="api"),
        MetadataDTO(name="Language", value="Python"),
        ]
    )

    qna6 = QnADTO(
    answer="We partner with the best independent hotels all across the world and can arrange accommodation that suits your needs and budget. From small boutique five-star luxury resorts, we’ve got the right hotel for you.",
    questions=["What hotels do you reserve?"],
    metadata=[
        MetadataDTO(name="Category", value="api"),
        MetadataDTO(name="Language", value="Python"),
        ]
    )

    qna7 = QnADTO(
    answer="Margie’s Travel partners with Humongous Insurance Corp. to provide travel insurance at competitive rates.",
    questions=["What travel insurance do you have?"],
    metadata=[
        MetadataDTO(name="Category", value="api"),
        MetadataDTO(name="Language", value="Python"),
        ]
    )

    qna8 = QnADTO(
    answer="Our agents are available by phone on 555 123 456 Monday to Friday from 8:00am to 6:00pm PST. You get help on our website at www.margiestravel.com 24x7.",
    questions=["How can I contact a travel agent?"],
    metadata=[
        MetadataDTO(name="Category", value="api"),
        MetadataDTO(name="Language", value="Python"),
        ]
    )

    urls = []

    create_kb_dto = CreateKbDTO(
        name="AI KM QnA Maker",
        qna_list=[qna1, qna2, qna3, qna4, qna5, qna6, qna7, qna8],
        urls=urls,
        files=[],
        enable_hierarchical_extraction=True,
        default_answer_used_for_extraction="No answer found.",
        language="English"
    )
    create_op = client.knowledgebase.create(create_kb_payload=create_kb_dto)

    create_op_monitor = _monitor_operation(client=client, operation=create_op)

    # Get knowledge base ID from resourceLocation HTTP header
    knowledge_base_ID = create_op_monitor.resource_location.replace("/knowledgebases/", "")
    print("Created KB with ID: {}".format(knowledge_base_ID))

    return knowledge_base_ID

#Download KB
def download_kb(client, kb_id):
    print("Downloading knowledge base...")
    kb_data = client.knowledgebase.download(kb_id=kb_id, environment="Prod")
    print("Downloaded knowledge base. It has {} QnAs.".format(len(kb_data.qna_documents)))

#Publish KB to Azure
def publish_kb(client, kb_id):
    print("Publishing knowledge base...")
    client.knowledgebase.publish(kb_id=kb_id)
    print("Published knowledge base.")

#Get query runtime key
def getEndpointKeys_kb(client):
    print("Getting runtime endpoint keys...")
    keys = client.endpoint_keys.get_keys()
    print("Primary runtime endpoint key: {}.".format(keys.primary_endpoint_key))

    return keys.primary_endpoint_key

#Generate an answer from the KB
def generate_answer(client, kb_id, runtimeKey):
    print ("Querying knowledge base...")

    authHeaderValue = "EndpointKey " + runtimeKey

    listSearchResults = client.runtime.generate_answer(kb_id, QueryDTO(question = "How can I contact a travel agent?"), dict(Authorization=authHeaderValue))

    for i in listSearchResults.answers:
        print(f"Answer ID: {i.id}.")
        print(f"Answer: {i.answer}.")
        print(f"Answer score: {i.score}.")

#Delete KB from Azure
def delete_kb(client, kb_id):
    print("Deleting knowledge base...")
    client.knowledgebase.delete(kb_id=kb_id)
    print("Deleted knowledge base.")