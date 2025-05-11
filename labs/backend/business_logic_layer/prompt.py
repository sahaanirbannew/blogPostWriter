class Prompt: 
    def __init__(self):
        self.prompt = ""
    
    def return_describe_image(self, place, date = "recently", time = "the morning"):
        prompt = """
            You are a naturalist.
            You will be given an photograph.
            (b/a) means "bird or animal"

            The photograph is taken in """ + place + """, on """ + date +  """ at """ + time + """. So make sure the (b/a) you predict, can be found in the region.

            If the photograph contains a (b/a), return the following details in the following format:
            {
            "isWild": { 
                "isWild": <True if the detected object is an (b/a), False otherwise>, 
                "isBird": <True if the image contains a bird, False otherwise>,
                "location": < location of the (b/a) in the image. Format: place, state, country >, 
                }, 
            "species_description": {
                "name": < name of the (b/a). Put "N.A" if isWild is False.>,
                "gender": <male/ female/ N.A>, 
                "likelihood": < likelihood of the prediction being true. It should be a float between 0 and 1. >, 
                "scientific_name": < scientific name of the (b/a) >,
                "wikipedia_link": < wikipedia link >,
                "keywords": [< list of keywords. Keywords should include species name, IUCN status, relevant keywords, predominant colours.>] 
            }, 
            "image_description": {
                "description": <describe what the (b/a) are doing in this image. Be very descriptive. Mention the date and time if available. Mention any action if you are able to.>, 
                "alt_text": <write an alt text for the image.>, 
                "caption": <write a caption for the image. Be precise>, 
                "keywords": [< list of keywords. Keywords should include elements in the photo, relevant keywords, predominant colours.>]
            }
            "species_fact": {
                "fascinating_fact": < mention a fascinating fact of the (b/a) probably linked to the location AND the image_description's description.>, 
                "citation": < give the link to the citation for the fascinating face you have given. >, 
                "extract": <extract from the citation which mentions the fascinating fact.>
                }, 
            
            "closest_species": {
                "name": < mention the species closest to this (b/a) by looks or behaviour >,
                "difference": < mention the differences between the (b/a) and the closest species. >,
                "citation": < give the link to the citation for the closest species. >,
                "extract": <extract from the citation which mentions the fascinating fact.>
            },
            "reasoning":{
                "reason": < reason for the species prediction/score of the likelihood. Be explicit here. Talk about the visible features of the (b/a). >,
                "citation": < give the link to the citation for the reason you mentioned above. >
            }
            }

            If it does not have a bird in the image, then return the following:
            {
            "name": "no (b/a) found",
            "keywords": [< list of keywords. Keywords should include elements in the photo, relevant keywords, predominant colours.>]
            } 
            """
        return prompt 