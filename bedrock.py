import boto3
from botocore.exceptions import ClientError
import json

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-west-2")
class bedrock_actions:

    def converse(prompt, image_format, encoded_image, max_tokens, temperature, top_p):
        try:
            response = bedrock_runtime.converse(
                modelId='anthropic.claude-3-haiku-20240307-v1:0',
                messages=[
                    {
                        'role': 'user',
                        'content': [
                            {
                                'text': prompt,
                            },
                            {
                                'image': {
                                    'format': image_format,
                                    'source': {
                                        'bytes': encoded_image
                                    }
                                },
                            }
                        ]
                    },
                ],
                inferenceConfig={
                    'maxTokens': int(max_tokens),
                    'temperature': float(temperature),
                    'topP': float(top_p),
                },
                )
            return response
        except ClientError as e:
            print("Failed to converse")
            print(e)
            return False