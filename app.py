from flask import Flask, render_template, request
from azure.identity import ClientSecretCredential
from azure.mgmt.media import AzureMediaServices
import random
from azure.mgmt.media.models import (
    IPRange,
    IPAccessControl,
    LiveEvent,
    LiveEventInputAccessControl,
    LiveEventPreviewAccessControl,
    LiveEventPreview,
    LiveEventInput,
    LiveEventEncoding,
    LiveEventEncodingType,
    LiveEventInputProtocol,
    StreamOptionsFlag
)

app = Flask(__name__)

# Tenant ID for your Azure Subscription
TENANT_ID = "31091900-0d4d-423b-b04e-fe4201c763bd"

# Your Application Client ID of your Service Principal
CLIENT_ID = "49252a39-ed92-45a1-9427-4b456fa3a4d7"

# Your Service Principal secret key
CLIENT_SECRET = "MLm8Q~51.W7AuZOzeZNDHqIsl-whM32gGc1X7aGj"

# Get the environment variables
subscription_id = "39c41e42-c205-40c1-b1bc-ef2eac9429b3"
resource_group ="Digiplus"
account_name ="digipluscamera"

uniqueness = random.randint(0,9999)
prefix = "myLiveEvent1"
live_event_name = f'{prefix}-{uniqueness}'

@app.route("/liveStart/")
def main():

    client = AzureMediaServices(
        credential=ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET),
        subscription_id="39c41e42-c205-40c1-b1bc-ef2eac9429b3",
    )

    response = client.live_events.begin_start(
        resource_group_name=resource_group,
        account_name=account_name,
        live_event_name=live_event_name,
    ).result()
    output = str(response)

    live_output_name = 'myOutput1'
    response1 = client.live_outputs.begin_create(
        resource_group_name=resource_group,
        account_name=account_name,
        live_event_name=live_event_name,
        live_output_name=live_output_name,
        parameters={
            "properties": {
                "archiveWindowLength": "PT5M",
                "assetName": "myAsset1",
                "description": "test live output 1",
                "hls": {"fragmentsPerTsSegment": 5},
                "manifestName": "testmanifest",
                "rewindWindowLength": "PT4M",
            }
        },
    ).result()
    output1 = str(response1)
    return render_template("script.html")
    
@app.route("/liveStop/")
def stop():
    
    client = AzureMediaServices(
        credential=ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET),
        subscription_id="39c41e42-c205-40c1-b1bc-ef2eac9429b3",
    )

    response = client.live_events.begin_stop(
        resource_group_name=resource_group,
        account_name=account_name,
        live_event_name=live_event_name,
        parameters={"removeOutputsOnStop": True},
    ).result()
    output = str(response)
    return render_template("script.html")
