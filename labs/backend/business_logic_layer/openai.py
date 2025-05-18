from business_logic_layer.config import Config
from openai import OpenAI 
import base64
config = Config()

print(config)

class OpenAIOps:
    def __init__(self):
        self.openai_key = config.openai.api_key
        self.openai_model = config.openai.model
        self.client = OpenAI(api_key=self.openai_key)

    def encode_image_to_base64(self, image_path):
        """Reads an image file and encodes it to a base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    def describe_image(self, image_path, prompt, max_tokens, response_format, temperature=0.0): 
        base64_image = self.encode_image_to_base64(image_path) 
        response = self.client.chat.completions.create(
            model=self.openai_model,  # Vision-enabled
            messages=[
                {
                    "role": "user",
                    "content": [
                        { "type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content