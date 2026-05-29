import urllib.request
import os

def main():
    url = "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation/resolve/main/zomato.csv"
    dest_dir = "data"
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, "zomato.csv")
    
    print(f"Downloading dataset from: {url}")
    print(f"Saving to: {dest_path}")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            meta = response.info()
            file_size = meta.get("Content-Length")
            if file_size:
                file_size = int(file_size)
                print(f"File size: {file_size / (1024 * 1024):.2f} MB")
            else:
                print("File size unknown")
                
            # Download file in chunks
            chunk_size = 1024 * 1024 # 1MB chunks
            downloaded = 0
            with open(dest_path, "wb") as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if file_size:
                        print(f"Downloaded: {downloaded / (1024 * 1024):.2f} MB / {file_size / (1024 * 1024):.2f} MB ({downloaded/file_size*100:.1f}%)", end="\r")
                    else:
                        print(f"Downloaded: {downloaded / (1024 * 1024):.2f} MB", end="\r")
            print("\nDownload complete!")
            
            # Read first few lines of CSV
            print("\nFirst 3 lines of the CSV file:")
            with open(dest_path, "r", encoding="utf-8", errors="ignore") as f:
                for i in range(3):
                    line = f.readline()
                    if not line:
                        break
                    print(f"Line {i+1}: {line.strip()}")
                    
    except Exception as e:
        print("Error downloading file:", e)

if __name__ == "__main__":
    main()
