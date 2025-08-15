import os
import requests

url = "http://localhost:8000/api/v1/basic/upload-for-gallery"

for file in os.listdir("images/test"):
    with open(f"images/test/{file}", "rb") as f:
        response = requests.post(url, files={"file": f}, timeout=1000)
        print(response.json())

# TODO: reupload images and make sure items is populated
