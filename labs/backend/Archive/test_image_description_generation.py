from business_logic_layer.image_ import ImageFinal 


date = "21 March 2025"
place = "Latpanchar" 
time = "08:45:56 hours"
path = "/Users/anirbansaha/Dropbox/copy_Latpanchar 2025 - experiment/DSC_6320-Enhanced-NR.jpg"  # Replace with your image path
image = ImageFinal(date, place, time, path)

print(image.description.species_description.name) 