import requests
import os
import sys

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Successfully downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_image.py <url> <save_path>")
        sys.exit(1)
    
    url = sys.argv[1]
    save_path = sys.argv[2]
    download_image(url, save_path)
