import requests
import json
import time

def save_to_web_archive(preload_urls, delay_seconds=10):
    save_url = 'https://web.archive.org/save'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://web.archive.org',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    for preload_url in preload_urls:
        # Record the start time
        start_time = time.time()


        data = {
            'url_preload': preload_url,
        }

        response = requests.post(save_url, headers=headers, data=data)

        # Check the response
        if response.status_code == 200:
            print(f"Saved {preload_url} to web archive.")
        else:
            print(f"Failed to save {preload_url} with status code {response.status_code}.")

        # Record the end time
        end_time = time.time()

        # Calculate and display the total execution time
        execution_time = end_time - start_time
        print(f"Preloading finished. Total execution time: {execution_time:.2f} seconds")


        # Add a delay between submissions
        time.sleep(delay_seconds)


def submit_url_to_web_archive(preload_urls, delay_seconds=10):
    for preload_url in preload_urls:
        # Record the start time
        start_time = time.time()

        submit_url = f'https://web.archive.org/save/{preload_url}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://web.archive.org',
            'Referer': 'https://web.archive.org/save',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        data = {
            'url': preload_url,
            'capture_outlinks': '1',
            'capture_all': 'on',
            'capture_screenshot': 'on',
            'wm-save-mywebarchive': 'on',
        }

        response = requests.post(submit_url, headers=headers, data=data)

        # Check the response
        if response.status_code == 200:
            print(f"Submitted {preload_url} to web archive.")
        else:
            print(f"Failed to submit {preload_url} with status code {response.status_code}.")

        # Record the end time
        end_time = time.time()

        # Calculate and display the total execution time
        execution_time = end_time - start_time
        print(f"Preloading finished. Total execution time: {execution_time:.2f} seconds")

        # Add a delay between submissions
        time.sleep(delay_seconds)

def check_preload_url_snapshot(preload_url):
    # Remove "https://" protocol if present
    preload_url_no_protocol = preload_url.replace('https://', '')

    api_url = f'https://archive.org/wayback/available?url={preload_url}'
    api_url_no_protocol = f'https://archive.org/wayback/available?url={preload_url_no_protocol}'

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        archived_snapshots = data.get('archived_snapshots', {})
        closest_snapshot = archived_snapshots.get('closest', {})
        if closest_snapshot:
            return closest_snapshot

     # If not found, try with the URL without the protocol
    response_no_protocol = requests.get(api_url_no_protocol)

    if response_no_protocol.status_code == 200:
        data_no_protocol = response_no_protocol.json()
        archived_snapshots_no_protocol = data_no_protocol.get('archived_snapshots', {})
        closest_snapshot_no_protocol = archived_snapshots_no_protocol.get('closest', {})
        return closest_snapshot_no_protocol
    
    return None

def check_all_preload_url(preload_urls):
    while preload_urls:
        url_to_check = preload_urls[0]  # Get the first URL from the list
        closest_snapshot = check_preload_url_snapshot(url_to_check)
        
        if closest_snapshot:
            print(f"Snapshot found for URL: {url_to_check}")
            print(f"Status: {closest_snapshot.get('status')}")
            print(f"Timestamp: {closest_snapshot.get('timestamp')}")
            preload_urls.pop(0)  # Remove the checked URL from the list
        else:
            print(f"No snapshot found for URL: {url_to_check}")
        
        if preload_urls:
            print("Waiting for the next URL...")
            time.sleep(10)  # Adjust the delay as needed


# Read preload URLs from a JSON configuration file
def read_preload_urls_from_config(config_file):
    with open(config_file, 'r') as file:
        config_data = json.load(file)
        preload_urls = config_data.get('preload_urls', [])
    return preload_urls

def main():
    config_file = 'preload_config.json'
    preload_urls = read_preload_urls_from_config(config_file)
    # save_to_web_archive(preload_urls, delay_seconds=10)
    submit_url_to_web_archive(preload_urls, delay_seconds=10)
    check_all_preload_url(preload_urls)

if __name__ == "__main__":
    main()
