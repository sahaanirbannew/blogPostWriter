from business_logic_layer.logger import logger   
from business_logic_layer.image_ import ImageInitial as ImageAS 
from business_logic_layer.image_ import ImageFinal 
from business_logic_layer.folder import Folder
image_extensions = ImageAS.image_extensions  # Set of image file extensions 
import pandas as pd

def process_folder(folder_path):
    place = input("Enter the name of the place: ")  # Get the place name from the user
    if not place:
        logger.error("❌ Place name cannot be empty.")
        return False 

    folder = Folder(folder_path, place)        # Create a Folder object 
    
    if not folder.isValid:              # Check if the folder is valid. Return if Invalid. 
        logger.error(f"❌ Invalid folder: {folder_path}")
        return False 
    
    if len(folder.imageFiles) == 0:        # Check if the folder has image files. Return if empty.
        logger.error(f"❌ No image files found in the folder: {folder_path}")
        return False
    logger.info(f"✅ Image files found in the folder: {folder_path}") 

    # Copy the Folder. 
    logger.info(f"✅ Copying folder: {folder.path} to {folder.copiedPath}")  

    # Printing the Exif Data. 
    images_pd = folder.exifData_pd 
    images_pd.to_csv("images_metadata_output.csv", index=False)


    data = [] 
    for _, row in images_pd.iterrows(): 
        try: 
            image_path = row['full_path'] 
            date = row['date'] 
            if not date:
                date = "Unknown"  # Handle missing date
            time = row['time']  
            if not time:
                time = "Unknown"  # Handle missing time
            aspect_ratio = row['aspect_ratio'] 
            place = row['place']
            logger.info(place)
            image = ImageFinal(date, place, time, image_path)  # Create an ImageFinal object 
            data.append({
                "date": date,
                "place": place,
                "time": time,
                "aspect_ratio": aspect_ratio,
                "image_path": image_path, 
                "species_name": image.description.species_description.name,
                "species_gender": image.description.species_description.gender,
                "species_scientific_name": image.description.species_description.scientific_name,
                "species_wikipedia_link": image.description.species_description.wikipedia_link,
                "species_keywords": image.description.species_description.keywords,
                "image_description": image.description.image_description.description,
                "image_alt_text": image.description.image_description.alt_text,
                "image_caption": image.description.image_description.caption,
                "species_fact": image.description.species_fact,
                "closest_species": image.description.closest_species,
                "reasoning": image.description.reasoning.reason, 
                "new_file_name": image.new_file_name
            })
        except Exception as e:
            logger.error(f"❌ Failed to process image {image_path}: {e}")
            continue 
    # Convert the data to a DataFrame
    images_final_pd = pd.DataFrame(data) 
    images_final_pd.to_csv("images_final_output.csv", index=False) 
    return True 

if __name__ == "__main__":
    folder_path = "/Users/anirbansaha/Dropbox/Latpanchar 2025 - experiment"  # Replace with your folder path
    process_folder(folder_path)