from business_logic_layer.logger import logger, log_exception
import os 
import pandas as pd
import shutil  
from business_logic_layer.image_ import ImageInitial as ImageAS
from business_logic_layer.generic import format_datetime  
import re 

image_extensions = ImageAS.image_extensions  # Set of image file extensions 

class Folder():
    def __init__(self, path, place):
        self.place = place 
        self.path = path  
        self.isValid = self.is_valid() 
        self.copiedPath = self.copy_folder() 
        self.path = self.copiedPath
        self.imageFiles = self.get_image_files() 
        self.exifData_pd = self.extract_exif_data()

    def is_valid(self):
        if not os.path.isdir(self.path):
            logger.error(f"❌ Not a valid directory: {self.path}") 
            return False
        if not os.access(self.path, os.R_OK):
            logger.error(f"❌ No read access to: {self.path}")
            return False 
        logger.info(f"✅ Valid and accessible directory: {self.path}")  

        return True  

    def copy_folder(self):
        base_name = os.path.basename(self.path.rstrip('/'))
        parent_dir = os.path.dirname(self.path)
        copy_folder = os.path.join(parent_dir, f"copy_{base_name}") 
        os.makedirs(copy_folder, exist_ok=True) 

        for file in os.listdir(self.path):
            file_path = os.path.join(self.path, file)
            if os.path.isfile(file_path) and os.path.splitext(file.lower())[1] in image_extensions: 
                shutil.copy2(file_path, copy_folder)  # ✅ preserves EXIF 
        return copy_folder  
    
    def get_image_files(self):
        image_files = [] 
        if self.isValid == True: 
            for file in os.listdir(self.path):
                    full_path = os.path.join(self.path, file)   
                    if os.path.isfile(full_path) and os.path.splitext(file.lower())[1] in image_extensions:
                        image_files.append(full_path)
                        logger.info(f" - {full_path}")
        return image_files 

    def extract_exif_data(self):
        metadata_list = []  
        for image_path in self.imageFiles: 
            new_image = ImageAS(image_path, self.place)    
            metadata = new_image.metadata
            metadata_list.append(metadata)

        df = pd.DataFrame(metadata_list) 

        # Clean up the DataFrame 
        df = df[df['aspect_ratio'] > 1] 
        df = self.cleanup_images(df) 
        return df
    
    def extract_unique_id(self, filename):
        """Extract the unique identifier from filename like 'DSC_123-Enhanced-NR.jpg' or 'DSC_123-2.jpg'."""
        match = re.search(r"DSC_(\d+)", filename)
        return match.group(1) if match else None

    def version_score(self, filename):
        """Return a score for sorting: png > -2 > original jpg"""
        if filename.lower().endswith(".png"):
            return 3
        if "-2" in filename:
            return 2
        return 1
    
    def cleanup_images(self, df):
        if "file_name" not in df.columns:
            raise ValueError("DataFrame must contain a 'file_name' column")

        df["unique_id"] = df["file_name"].apply(self.extract_unique_id)
        df["version_score"] = df["file_name"].apply(self.version_score)

        # Sort by unique_id and version_score descending
        df_sorted = df.sort_values(by=["unique_id", "version_score"], ascending=[True, False])

        # Keep only the top version for each unique_id
        df_cleaned = df_sorted.drop_duplicates(subset=["unique_id"], keep="first").reset_index(drop=True)

        # Drop helper columns if not needed
        df_cleaned = df_cleaned.drop(columns=["version_score", "unique_id"])

        # Add place name to the DataFrame 
        df_cleaned["place"] = self.place

        return df_cleaned