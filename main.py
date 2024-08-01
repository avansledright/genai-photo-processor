import sys
import os
from bedrock import bedrock_actions
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        image_file.close()
    return encoded_string
def modify_product_name(product_name):
    # Replace spaces with hyphens
    product_name = product_name.replace(' ', '-')
    # Remove single quotes
    product_name = product_name.replace("'", "")
    # Replace ampersands with hyphens
    product_name = product_name.replace('&', '-')
    # Convert to lowercase
    product_name = product_name.lower()
    return product_name

if __name__ == "__main__":
    print("Processing images")
    files = os.listdir("photos")
    print(len(files))
    for file in files:
        if file.endswith(".jpeg"):
            print(f"Sending {file} to Bedrock")
            with open(f"photos/{file}", "rb") as photo:

                prompt = f"""
                    Looking at the image included, find and return the name of the product. 
                    Rules: 
                    1. Return only the product name that has been determined.
                    2. Do not include any other text in your response like "the product determined..."
                    """
                model_response = bedrock_actions.converse(
                    prompt, 
                    image_format="jpeg",
                    encoded_image=photo.read(),
                    max_tokens="2000",
                    temperature=.01,
                    top_p=0.999
                    )
                print(model_response['output'])
                product_name = modify_product_name(model_response['output']['message']['content'][0]['text'])
                
                photo.close()
                if os.system(f"cp photos/{file} renamed_photos/{product_name}.jpeg") != 0:
                    print("failed to move file")
                else:
                    os.system(f"mv photos/{file} finished/{file}")
    sys.exit(0)