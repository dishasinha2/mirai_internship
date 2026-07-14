import requests
prompt="Virat Kohli winning the world cup 2027 with indian team"

url=f"https://image.pollinations.ai/prompt/{prompt}"

print(f"Generating image...{prompt}")
response=requests.get(url)
print(response)
if response.status_code==200:
    with open("Goat.png","wb") as file:
        file.write(response.content)
    print("Success")
else:
    print("Failed to generate image")