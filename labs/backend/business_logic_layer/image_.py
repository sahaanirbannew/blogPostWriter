import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import pandas as pd
from PIL import Image
import piexif 
import os, re, json 
from datetime import datetime  
from business_logic_layer.logger import logger
from business_logic_layer.prompt import Prompt
from business_logic_layer.openai import OpenAIOps
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Literal, Optional

class IsWild(BaseModel):
    isWild: bool
    isBird: bool
    location: str

class SpeciesDescription(BaseModel):
    name: str
    gender: Literal['male', 'female', 'male and female', 'N.A']
    likelihood: float
    scientific_name: str
    wikipedia_link: HttpUrl
    keywords: List[str]

class ImageDescription(BaseModel):
    description: str
    alt_text: str
    caption: str
    keywords: List[str]

class SpeciesFact(BaseModel):
    fascinating_fact: str
    citation: HttpUrl
    extract: str

class ClosestSpecies(BaseModel):
    name: str
    difference: str
    citation: HttpUrl
    extract: str

class Reasoning(BaseModel):
    reason: str
    citation: HttpUrl

class PredictionResponse(BaseModel):
    isWild: IsWild
    species_description: SpeciesDescription
    image_description: ImageDescription
    species_fact: SpeciesFact
    closest_species: ClosestSpecies
    reasoning: Reasoning

def clean_and_parse_json(response_text: str):
    """
    Cleans a string returned by OpenAI that starts with ```json and ends with ```
    and parses the JSON inside.
    """
    # Remove backticks and 'json' if present
    response_text = response_text.strip()
    response_text = re.sub(r"^```json", "", response_text, flags=re.IGNORECASE).strip()
    response_text = re.sub(r"```$", "", response_text).strip()

    # Find the first JSON object in the string using regex
    match = re.search(r"({.*})", response_text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in the response.")
    
    json_string = match.group(1)
    
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON: {e}\nRaw input:\n{json_string}")
    
def validate_openai_response_string(raw_response: str): 
    parsed_json = clean_and_parse_json(raw_response)
    try:
        validated = PredictionResponse(**parsed_json)
        return validated
    except Exception as e:
        logger.error("Validation failed:", e)
        raise

class ImageFinal:
    def __init__(self, date, place, time, path, max_size = 1300):
        self.date = date 
        self.place = place
        self.time = time
        self.path = path
        self.max_size = max_size 

        self.alt_text = None
        self.caption = None
        self.description = None

        self.resize_image() # Resize the image to the max size 

        self.prompt = Prompt().return_describe_image(self.place, self.date, self.time) 
        self.description = self.get_image_description_using_llm() 

        _, ext = os.path.splitext(self.path) 
        self.new_file_name = self.description.species_description.name + "_" + self.place + "_" +  self.date + "_" + self.time + ext
        logger.info(f"Image description: {self.description}")
         
    def get_image_description_using_llm(self): 
        llm = OpenAIOps()
        response = llm.describe_image(
            image_path=self.path,
            prompt=self.prompt,
            max_tokens=4000,
            response_format="json",
            temperature=0.0
        )
        response = response.replace("\n", "")  
        validated_response = validate_openai_response_string(response)
        return validated_response


    def resize_image(self):
        max_size = self.max_size 
        try:
            with Image.open(self.path) as img:
                width, height = img.size
                if width > height:
                    new_width = max_size
                    new_height = int((max_size / width) * height)
                else:
                    new_height = max_size
                    new_width = int((max_size / height) * width)

                resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                resized_img.save(self.path)
                logger.info(f"✅ Resized: {self.path} to {new_width}x{new_height}")
        except Exception as e:
            logger.error(f"❌ Failed to resize {self.path}: {e}")




class ImageInitial:
    def __init__(self, image_path: str, place: str = None):
        self.date = None 
        self.time = None 
        self.aspectRatio = None 

        self.path = image_path  
        self.metadata = self.extract_image_metadata() 
        self.place = place
        
        self.description = None
        self.alt_text = None 
        self.caption = None 

    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    
    def get_aspect_ratio(self, width, height):
        ratio = round(width / height, 2)
        return ratio
    
    def extract_image_metadata(self):
        metadata = {
            "file_name": os.path.basename(self.path),
            "full_path": self.path,
            "date": None, 
            "time": None,
            "aspect_ratio": None
        }

        try:
            img = Image.open(self.path)
            width, height = img.size
            self.aspectRatio = self.get_aspect_ratio(width, height) 
            metadata["aspect_ratio"] = self.aspectRatio
            exif_data = piexif.load(img.info["exif"])

            # 1. Date and Time
            date_taken = exif_data["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
            if date_taken:
                #metadata["datetime"] = date_taken.decode('utf-8') 
                decoded_date = date_taken.decode('utf-8')
                try:
                    dt = datetime.strptime(decoded_date, "%Y:%m:%d %H:%M:%S")
                    self.date = dt.strftime("%d %B %Y")             # e.g., "21 March 2025"
                    self.time = dt.strftime("%H:%M:%S") + " hours"  # e.g., "08:45:56 hours"
                except ValueError:
                    self.date = None
                    self.time = None 
            else: 
                self.date = None
                self.time = None
            
            metadata["date"] = self.date 
            metadata["time"] = self.time


            # 2. GPS Info
            gps_data = exif_data.get("GPS")
            if gps_data:
                def _convert_to_degrees(values):
                    d, m, s = values
                    return d[0]/d[1] + (m[0]/m[1])/60 + (s[0]/s[1])/3600

                gps_lat = gps_data.get(piexif.GPSIFD.GPSLatitude)
                gps_lat_ref = gps_data.get(piexif.GPSIFD.GPSLatitudeRef)
                gps_lon = gps_data.get(piexif.GPSIFD.GPSLongitude)
                gps_lon_ref = gps_data.get(piexif.GPSIFD.GPSLongitudeRef)

                if gps_lat and gps_lat_ref and gps_lon and gps_lon_ref:
                    lat = _convert_to_degrees(gps_lat)
                    if gps_lat_ref.decode() != "N":
                        lat = -lat

                    lon = _convert_to_degrees(gps_lon)
                    if gps_lon_ref.decode() != "E":
                        lon = -lon

                    # metadata["latitude"] = lat
                    # metadata["longitude"] = lon

        except Exception as e:
            print(f"❌ Error reading {self.path}: {e}")
        return metadata 