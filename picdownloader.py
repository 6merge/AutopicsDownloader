import os
import requests

def download_images(query, n, output_folder, api_key):
    # Base URL for the Unsplash API
    url = f"https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {api_key}"}
    
    # Create the folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        print(f"Searching for '{query}' images...")
        response = requests.get(url, params={"query": query, "per_page": n}, headers=headers)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        
        if not results:
            print("No images found for your query.")
            return
        
        print(f"Found {len(results)} images. Downloading...")
        
        for idx, image in enumerate(results[:n], start=1):
            image_url = image["urls"]["regular"]
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            file_path = os.path.join(output_folder, f"{query}_{idx}.jpg")
            with open(file_path, "wb") as file:
                file.write(image_response.content)
            
            print(f"Downloaded {file_path}")
            
        print(f"All {n} images downloaded successfully into '{output_folder}'!")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Input your API key and other parameters
API_KEY = "2C1VtXr6bpSeIScXBdwaF0vssf5rVQo2OPgdjpnmu2w"  # Replace with your Unsplash API key
query = input("Enter the search query: ")
n = int(input("Enter the number of images to download: "))
output_folder = "./downloaded_images"

# Run the downloader
download_images(query, n, output_folder, API_KEY)
