import requests
import json
import re
import base64
import boto3
import io
import uuid
def delete_s3(bucket="mealmakeraiimages"):
    s3_client = boto3.client('s3',
        aws_access_key_id='AKIAREZ56TUXCCKA424C',
        aws_secret_access_key='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',
        region_name='us-east-1'
    )
    
    # List all objects in the bucket
    objects = s3_client.list_objects_v2(Bucket=bucket)
    print(objects)
    # Delete all objects
    if 'Contents' in objects:
        for obj in objects['Contents']:
            s3_client.delete_object(Bucket=bucket, Key=obj['Key'])
            print(f"Deleted {obj['Key']}")
def upload_to_s3(image_bytes, file_name, bucket="mealmakeraiimages"):
    """Upload a file to an S3 bucket and return the URL"""
    s3_client = boto3.client('s3',
        aws_access_key_id='AKIAREZ56TUXCCKA424C',
        aws_secret_access_key='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',
        region_name='us-east-1'
    )
    s3 = boto3.resource('s3')


        # Upload the file
    s3_client.upload_fileobj(
        io.BytesIO(image_bytes),
        bucket,
        file_name,
        ExtraArgs={'ContentType': 'image/png'}
    )
    # Generate the URL
    url = s3.meta.client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': file_name},
        ExpiresIn=3600  # URL expires in 1 hour
    )
    return url
    
def safe_extract_json(raw_text):
    # Remove code block wrappers if present
    cleaned = re.sub(r"^```json\n?|```$", "", raw_text.strip(), flags=re.MULTILINE)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to extract the first valid-looking JSON object
        match = re.search(r'\{(?:[^{}]|(?R))*\}', cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return {"error": "Failed to parse JSON"}
def gen_recipe(prompt, api_key):
    OPENAI_API_KEY="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"
    # OpenAI API call for recipe generation
    url = "https://api.openai.com/v1/responses"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    payload = {
        "model": "gpt-4.1-nano",
        "input": prompt
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.json())
    if response.status_code == 200:
        recipe_data = safe_extract_json(response.json()['output'][0]['content'][0]['text'])
        image_prompt = recipe_data['image_description']
        
        # Gemini API call for image generation
        # ...existing image generation code...
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent?key=AIzaSyBySkCG5yLgtz4IANJySl5Y59Xxt9pdVWI"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": f"{image_prompt}, also make the image wide like a rectangle"}
                ]
            }],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
        }

        image_response = requests.post(url, headers=headers, json=payload)
        
        if image_response.status_code == 200:
            image_data = image_response.json()


            
            try:
                base64_data = image_data['candidates'][0]['content']['parts'][1]['inlineData']['data']
            except:
                    image_response = requests.post(url, headers=headers, json=payload)
                    if image_response.status_code == 200:
                        image_data = image_response.json()
                        try:
                            base64_data = image_data['candidates'][0]['content']['parts'][1]['inlineData']['data']
                        except:
                                print("No image data in response")
                                return recipe_data,"images/error.png"


            
            if base64_data:
                image_bytes = base64.b64decode(base64_data)
                unique_id = uuid.uuid4().hex[:8]
                file_name = f"{recipe_data['title'].replace(' ', '_')}_{unique_id}.png"
                recipe_data['image_name'] = file_name
                # Upload to S3 instead of saving locally
                s3_url = upload_to_s3(image_bytes, file_name)
                print(s3_url)
                
                if s3_url:
                    print(f"Image uploaded to: {s3_url}")
                    return recipe_data,s3_url
                else:
                    print("Failed to upload image to S3")
                    return recipe_data,"images/error.png"
            else:
                print("No image data in response")
                return recipe_data,"images/error.png"
        else:
            print(f"Error generating image: {image_response.status_code}")
            print(image_response.text)
            return recipe_data,"images/error.png"
    else:
        print(f"Error generating recipe: {response.status_code}")
        print(response.text)
        return None,"images/error.png"
def delete_recipe_image(file_name, bucket="mealmakeraiimages"):
    s3_client = boto3.client('s3',
        aws_access_key_id='AKIAREZ56TUXCCKA424C',
        aws_secret_access_key='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',
        region_name='us-east-1'
    )
    try:
        s3_client.delete_object(Bucket=bucket, Key=file_name)
        print(f"Deleted recipe image: {file_name}")
        objects = s3_client.list_objects_v2(Bucket=bucket)
        print(objects)
    except Exception as e:
        print(f"Error deleting recipe image: {e}")