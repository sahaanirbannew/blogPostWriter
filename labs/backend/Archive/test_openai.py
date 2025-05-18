import business_logic_layer.openai as llm 


LLM = llm.OpenAIOps()

print(LLM.openai_key)

image_path = "labs/backend/DSC_6362-Enhanced-NR.jpg"
prompt = "Describe the image in detail." 
max_tokens = 1000
response_format = "text"
temperature = 0.0
response = LLM.describe_image(image_path, prompt, max_tokens, response_format, temperature)
print(response)
# print(response.choices[0].message.content)
