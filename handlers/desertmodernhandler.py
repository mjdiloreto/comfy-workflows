import random
import time
import os
from handlers.basehandler import BaseHandler
from utils.filesystem import Filesystem

"""
Handler classes are generally bound to a specific workflow file.
To modify values we have to be confident in the json structure.

One exception - RawWorkflow will send payload['workflow_json'] to the ComfyUI API after
downloading any URL's to the input directory and replacing the URL with a local path.
"""

class DesertModernHandler(BaseHandler):

    WORKFLOW_JSON = "/opt/serverless/workflows/matt-desert-runpod-api.json"

    def __init__(self, payload):
        super().__init__(payload, self.WORKFLOW_JSON)
        self.apply_modifiers()


    def apply_modifiers(self):
        # This will download the image and put it in the input dir
        self.temp_file =  self.get_value(
            "input_image",
            ""
        )

        self.prompt["prompt"]["429"]["inputs"]["image"] = self.temp_file

    def handle(self):
        try:
           return super().handle()
        finally:
            if self.temp_file:
                print("cleaning up temp files")
                Filesystem.remove_input_file(self.temp_file)




"""
Example Request Body:

{
    "input": {
        "handler": "DesertModernHandler",
        "aws_access_key_id": "your-s3-access-key",
        "aws_secret_access_key": "your-s3-secret-access-key",
        "aws_endpoint_url": "https://my-endpoint.backblaze.com",
        "aws_bucket_name": "your-bucket",
        "aws_key_prefix": "/subfolder/in/bucket/",
        "webhook_url": "your-webhook-url",
        "webhook_extra_params": {},
        "input_image": "https://raw.githubusercontent.com/comfyanonymous/ComfyUI/master/input/example.png"
    }
}

"""
