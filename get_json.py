from dotenv import load_dotenv

# for managing gemini api
from google import genai

# utils
from utils.images import resize_image_with_max

load_dotenv()

client = genai.Client()

IMG_PATH = './assets/amelie_still.jpg'

response = client.models.generate_content(
	model='gemini-2.0-flash',
	contents=[
     	'Caption this image.',
		resize_image_with_max(IMG_PATH, 384),
	]
)

print(response.text)
