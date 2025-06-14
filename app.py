from flask import Flask, render_template, request
from azure.identity import ClientSecretCredential
from azure.mgmt.media import AzureMediaServices
import random, asyncio
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
from database import db_append_live, db_append_boutique, fetch_live, fetch_user, verify
app = Flask(__name__)

# Tenant ID for your Azure Subscription
TENANT_ID = <azure_tenant_id>

# Your Application Client ID of your Service Principal
CLIENT_ID = <azure_client_id>

# Your Service Principal secret key
CLIENT_SECRET = <azure_client_secrert>

# Get the environment variables
subscription_id = <azure_subscription_id>
resource_group ="Digiplus"
account_name ="digipluscamera"


@app.route("/liveStart/<live_name>")
def main(live_name):

    live_event_name = verify(live_name)

    client = AzureMediaServices(
        credential=ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET),
        subscription_id=subscription_id ,
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
    
@app.route("/liveStop/<live_name>")
def stop(live_name):
    
    live_event_name = verify(live_name)

    client = AzureMediaServices(
        credential=ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET),
        subscription_id=subscription_id ,
    )

    response = client.live_events.begin_stop(
        resource_group_name=resource_group,
        account_name=account_name,
        live_event_name=live_event_name,
        parameters={"removeOutputsOnStop": True},
    ).result()
    output = str(response)
    return render_template("script.html")


"""CREATION DU CANAL DU LIVE"""

@app.route('/liveCreate/', methods=['GET', 'POST'])
def liveCreate():

    if request.method == 'POST':
        #recuperation des données du formulaire
        form = request.form
        nameProp = form['name']

        #creation d'un nom de live personnalisé
        uniqueness = random.randint(0,9999)
        live_event_name = f'{nameProp}-{uniqueness}'

        accessToken=<access_token>

        allow_all_input_range=IPRange(name="AllowAll", address="0.0.0.0", subnet_prefix_length=0)

        live_event_input_access=LiveEventInputAccessControl(ip=IPAccessControl(allow=[allow_all_input_range]))

        live_event_preview=LiveEventPreview(access_control=LiveEventPreviewAccessControl(ip=IPAccessControl(allow=[allow_all_input_range])))

        # enregistrement des parametres de creation du live
        live_event_create=LiveEvent(
        location="East US",
        description="Sample 720P Encoding Live Event from Python SDK sample",
        use_static_hostname=True,
        input=LiveEventInput(
            streaming_protocol=LiveEventInputProtocol.RTMP,
            access_control=live_event_input_access,
            access_token=accessToken
        ),

        encoding=LiveEventEncoding(
            encoding_type=LiveEventEncodingType.PASSTHROUGH_STANDARD,
        ),
        preview=live_event_preview,
        stream_options=[StreamOptionsFlag.LOW_LATENCY]
    )
        client = AzureMediaServices(
        credential=ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET),
        subscription_id=subscription_id ,
        )

        # creation du live
        response3 = client.live_events.begin_create(
            resource_group_name=resource_group,
            account_name=account_name,
            live_event_name=live_event_name,
            parameters=live_event_create
        ).result()
        output3 = f"rtmp://{live_event_name}-{account_name}-usea.channel.media.azure.net:1935/live/{accessToken}"
        #sauvegarde des données à enregistrer dans la table Live
        user_data = {
            "urlRtmp" :  output3,
            "nomLive" : live_event_name,
            "proprietaire": nameProp
        }
        #sauvegarde des données du live dans la table live de la BD
        db_append_live(user_data)
        #sauvegarde des données dans la table Boutique de la BD
        db_append_boutique(form)

        return (output3,live_event_name)
    else:
        return(render_template('form.html'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
