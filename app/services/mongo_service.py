# services/mongo_service.py
import requests
from requests.auth import HTTPDigestAuth

def get_public_ip():
    response = requests.get("https://api.ipify.org")
    return response.text

def whitelist_ip_in_mongo(ip, atlas_api_key_public, atlas_api_key_private, atlas_group_id):
    try:
        resp = requests.post(
            f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{atlas_group_id}/accessList",
            auth=HTTPDigestAuth(atlas_api_key_public, atlas_api_key_private),
            json=[{'ipAddress': ip, 'comment': 'From PythonAnywhere'}]
        )
        if resp.status_code in (200, 201):
            print("MongoDB Atlas accessList request successful", flush=True)
        else:
            print(
                f"MongoDB Atlas accessList request problem: status code was {resp.status_code}, content was {resp.content}",
                flush=True
            )
    except Exception as e:
        print(f"Error while whitelisting IP in MongoDB Atlas: {str(e)}")