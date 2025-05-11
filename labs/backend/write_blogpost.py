import openai
from openai import OpenAI 
import pandas as pd
import webbrowser
import os

from business_logic_layer.config import Config
config = Config() 


# Step 1: Set your OpenAI API key
openai.api_key = config.openai.api_key

# Step 2: Define your travel experience text
travel_experience = """
-- 1. I took a train to New Jalpaiguri. From there I hired a cab to Kalijhora market. The guide Ujwal picked me up on his scooty and took me to Latpanchar. 
-- 2. Slightly after I reached, he got information from other guides that a Rufous-necked hornbill pair was spotted. 
-- 3. We went there. They were far above and it was difficult to spot the first time. But it was an incredible thrill once I saw the Hornbills for the first time this year. There was a male and a female and they were courting. This is the season of their courtship.
-- 4. The expectation was that they would mate. They did not. They flew away in the opposite direction. 
-- 5. That was the first day and I did not carry my tripod with me. This is for the first time I am getting used to the idea of making videos.
-- 6. After breakfast, I went back to the homestay to get some rest. At around 12 noon, Ujwal called again and asked me to get ready. I was ready anyway.
-- 7. He hurriedly came and we got on the 2-wheeler scooty. First we drove on roads that were properly made. Then he tried taking a shortcut. It was just downhill through which we drove. For some time I closed my eyes and started rewinding all the good memories in my life. 
-- 8. Suddenly he stopped the scooty and started running. I ran behind him. He is a native of the place, and is used to the terrain. I am not. But I couldnt also be slow, else I would have lost him in the middle of the jungle. I followed him as fast as possible. That meant, jumping over boulders, running on logs connecting two pieces of land, running through a path that is less than a foot long. Thankfully I was wearing my running shoes. I was not slow. 
-- 9. We reached a home and we walked up to the terrace. The male Hornbill saw us and was unhappy about it. The female went to the next branch. The male tried wooing her. Later they went to a branch in the behind tree. We followed them. After around 15 mins of observing them, the female flew away and with her, the male also flew away. 
-- 10. Ujwal ran in the direction of the hornbills. I ran behind him. We ran over 200 meters downhill to a place where there were a few fruit trees. Behind that place was a deeper valley and in front were a few trees with clear branches. The female sat on one tree and the male sat on another. After minutes of wait, the female came on the top of the tree where the male was sitting. Slowly she came near the male. After some time, they both flew away. But this is where I took the main photograph.
-- 11. During day 2, we ran and chased the hornbill almost the same way we did the previous day. But this time, we ran with a heavy tripod. 
-- 12. We found the hornbill near the same tree with fruits. I made videos of the male and the female exchanging fruits. 
-- 13. After some time, they sat on the same branch they did the previous day. I made video of them sitting on the branch and being playful during courting. After some time, they flew away. 
"""

# Step 3: Define instructions to write the blog post
blog_instructions = """
Write a travel blog post focussed on my birding experience. The domain of the blog is Birding. 
I traveled to Latpanchar, West Bengal, India. 
Tone: Informal, Conversational, as if it is thriller story, with some humour in it. 
The blog post should be at least 4000 words long. 
Include visual imagery and helpful tips for birding enthusiasts. 
To insert image, use the full_path of the image in the table below.
Make sure you add the alt text, and caption for each image. 
Add at least 3 images from the table below. Make sure you add interesting facts.  
Do not make too many headlines or paragraphs. 
Write long elaborate paragraphs focussing more on my experiences and supporting my experience with images.
Do NOT give tips for birders, etc. Focus only on my experience.
"""

# Step 4: Load CSV content (or define inline for this example)
csv_file_path = "images_final_output.csv"
df = pd.read_csv(csv_file_path) 
csv_html_table = df.to_html(index=False, escape=False)

# Step 5: Combine everything into a single prompt
full_prompt = f"""
Birding Experience:
{travel_experience}

Instructions:
{blog_instructions}

Select at least 3 relevant images, context, facts, information from this table:
{csv_html_table}

Format the final output as a complete HTML page.
"""

# Step 6: Call OpenAI API
client = OpenAI(api_key=config.openai.api_key)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": full_prompt}
    ],
    temperature=1,
    max_tokens=4000
)

html_content = response.choices[0].message.content

# Step 7: Save to HTML file
html_filename = "travel_blog.html"
with open(html_filename, "w", encoding="utf-8") as f:
    f.write(html_content)

# Step 8: Display the HTML file in the default browser
webbrowser.open('file://' + os.path.realpath(html_filename))
