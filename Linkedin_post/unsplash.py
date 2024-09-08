# import requests
# import os
# from PIL import Image
# from io import BytesIO

# def search_photos(query, client_id, num_photos):
#     url = f"https://api.unsplash.com/search/photos/?query={query}&per_page={num_photos}"
#     headers = {
#         "Authorization": f"Client-ID {client_id}"
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
#         data = response.json()
#         photos = []
#         for photo in data.get('results', []):
#             photos.append(photo['urls']['regular'])
#         return photos
#     except requests.exceptions.RequestException as e:
#         print("Error occurred during API request:", e)
#         return []

# def download_photos(photos, folder="photos"):
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#     for i, photo_url in enumerate(photos, 1):
#         try:
#             response = requests.get(photo_url)
#             response.raise_for_status()
#             image = Image.open(BytesIO(response.content))
#             image.save(os.path.join(folder, f"photo_{i}.jpg"))
#             print(f"Photo {i} downloaded successfully!")
#         except requests.exceptions.RequestException as e:
#             print(f"Error downloading photo {i}: {e}")

# def main():
#     query = input("Enter a keyword to search for photos: ")
#     client_id = "Vq3QmyNK_3bOh_NpQehngm52DbLtuJo3L2GTGdJjY5o"  # Replace this with your Unsplash API client ID
#     num_photos = 2  # Number of photos to download
#     photos = search_photos(query, client_id, num_photos)
#     download_photos(photos)

# if __name__ == "__main__":
#     main()


import autogen
import chromadb
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import requests

config_list = [
    {
        "model": "gpt-4-turbo-preview",
        "api_key": "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"
    }
]

llm_config_proxy = {
    "temperature": 0,
    "config_list": config_list,
}

assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config_proxy,
    system_message="You are a helpful assistant. Provide accurate answers based on the context. Respond 'Unsure about answer' if uncertain.",
)

def fetch_unsplash_image(query):
    api_key = "Vq3QmyNK_3bOh_NpQehngm52DbLtuJo3L2GTGdJjY5o"
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {api_key}"}
    params = {"query": query, "page": 1, "per_page": 1}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['results'][0]['urls']['regular'] if data['results'] else "No image found"
    return "Failed to retrieve images"

# Example usage within an AutoGen environment
image_query = "beautiful landscapes"
image_url = fetch_unsplash_image(image_query)
print("Fetched Image URL:", image_url)
