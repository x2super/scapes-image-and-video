import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from pystyle import Colors, Colorate, Center, Anime, Write


DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def fetch_messages(channel_id, token, limit=100, before=None):
    params = {"limit": limit}
    if before:
        params["before"] = before
    response = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers={"Authorization": f"{token}"}, params=params)
    if response.status_code != 200:
        print(Colorate.Horizontal(Colors.blue_to_red,"failed to fetch images and videos !"))
        return
    return response.json()

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(save_path, "wb") as f, tqdm(
        desc=f"Downloading {os.path.basename(save_path)}",
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            bar.update(len(data))
            f.write(data)

def process_attachment(attachment):
    file_url = attachment["url"]
    file_name = attachment["filename"]
    save_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    if not os.path.exists(save_path):
        download_file(file_url, save_path)

def download_media_from_channel(channel_id, token):
    last_message_id = None
    attachments = []
    
    while True:
        messages = fetch_messages(channel_id, token, before=last_message_id)
        if not messages:
            break
        for message in messages:
            attachments.extend(message.get("attachments", []))
        last_message_id = messages[-1]["id"]
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_attachment, attachments)

if __name__ == "__main__":
    banner = r"""
                                                                  
███████╗██╗░░██╗░█████╗░██╗░░░░░██╗░░░██╗░██████╗██╗██╗░░░██╗███████╗
██╔════╝╚██╗██╔╝██╔══██╗██║░░░░░██║░░░██║██╔════╝██║██║░░░██║██╔════╝
█████╗░░░╚███╔╝░██║░░╚═╝██║░░░░░██║░░░██║╚█████╗░██║╚██╗░██╔╝█████╗░░
██╔══╝░░░██╔██╗░██║░░██╗██║░░░░░██║░░░██║░╚═══██╗██║░╚████╔╝░██╔══╝░░
███████╗██╔╝╚██╗╚█████╔╝███████╗╚██████╔╝██████╔╝██║░░╚██╔╝░░███████╗
╚══════╝╚═╝░░╚═╝░╚════╝░╚══════╝░╚═════╝░╚═════╝░╚═╝░░░╚═╝░░░╚══════╝

Create Souce by : Kasawa
"""[1:]
    try:
        os.system('cls')
    except:
        os.system('clear')
    print(Colorate.Horizontal(Colors.cyan_to_blue,banner))
    token = input(Colorate.Horizontal(Colors.cyan_to_blue,"> Press to token : "))
    channel = input(Colorate.Horizontal(Colors.cyan_to_blue,"> Press to token : "))

    download_media_from_channel(channel, token)
    print(Colorate.Horizontal(Colors.cyan_to_green,"Success All Clip and images !"))
