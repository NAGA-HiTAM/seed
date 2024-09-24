import requests
import time
from colorama import init, Fore, Style
import sys
import os
import datetime
import pytz
import re

init(autoreset=True)

def print_welcome_message():
    print(Fore.GREEN + Style.BRIGHT + r"Jquery Akan Expired Jadi Harus Ganti Ganti Kalo GK Mau Capek Pake Sessions,Gk Ribet,Tapi Rawan Banned Telegram")
    print(Fore.WHITE + Style.BRIGHT + r"""
███╗   ██╗ █████╗  ██████╗  █████╗     ██╗  ██╗██╗████████╗ █████╗ ███╗   ███╗
""")
    print(Fore.BLACK + Style.BRIGHT + r"""
████╗  ██║██╔══██╗██╔════╝ ██╔══██╗    ██║  ██║██║╚══██╔══╝██╔══██╗████╗ ████║
""")
    print(Fore.WHITE + Style.BRIGHT + r"""
██╔██╗ ██║███████║██║  ███╗███████║    ███████║██║   ██║   ███████║██╔████╔██║
""")
    print(Fore.BLACK + Style.BRIGHT + r"""
██║╚██╗██║██╔══██║██║   ██║██╔══██║    ██╔══██║██║   ██║   ██╔══██║██║╚██╔╝██║
""")
    print(Fore.WHITE + Style.BRIGHT + r"""
██║ ╚████║██║  ██║╚██████╔╝██║  ██║    ██║  ██║██║   ██║   ██║  ██║██║ ╚═╝ ██║
""")
    print(Fore.WHITE + Style.BRIGHT + r"""
╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝
""")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


url_claim = 'https://elb.seeddao.org/api/v1/seed/claim'
url_balance = 'https://elb.seeddao.org/api/v1/profile/balance'
url_checkin = 'https://elb.seeddao.org/api/v1/login-bonuses'
url_upgrade_storage = 'https://elb.seeddao.org/api/v1/seed/storage-size/upgrade'
url_upgrade_mining = 'https://elb.seeddao.org/api/v1/seed/mining-speed/upgrade'
url_upgrade_holy = 'https://elb.seeddao.org/api/v1/upgrades/holy-water'
url_get_profile = 'https://elb.seeddao.org/api/v1/profile'

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
    'content-length': '0',
    'dnt': '1',
    'origin': 'https://cf.seeddao.org',
    'priority': 'u=1, i',
    'referer': 'https://cf.seeddao.org/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'telegram-data': 'tokens',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def load_credentials():
    try:
        with open('tokens.txt', 'r') as file:
            tokens = file.read().strip().split('\n')
        return tokens
    except FileNotFoundError:
        print(Fore.RED + "[ERROR]: File tokens.txt tidak ditemukan.")
        return []
    except Exception as e:
        print(Fore.RED + f"[ERROR]: Terjadi kesalahan saat memuat token: {str(e)}")
        return []
access_token = None
expires_in = 0

def get_dynamic_url_and_content():

    response = requests.get('https://tganalytics.xyz')
    if response.status_code == 200:

        new_url_suffix = re.search(r'/[a-f0-9]{32}', response.text)
        if new_url_suffix:
            return new_url_suffix.group(0), "123,34,97,34,58,54,44,34,98,34,58,53,56,125"
    return None, None

def refresh_token():
    global access_token, expires_in
    
    dynamic_url_suffix, dynamic_content = get_dynamic_url_and_content()
    if not dynamic_url_suffix or not dynamic_content:
        print("Gagal mengambil URL atau konten dinamis.")
        return
    
    payload = [
        {
            "event_name": "app-hide",
            "session_id": "0d475233-6062-457e-9140-5257e1140525",
            "user_id": 6973178056,
            "app_name": "seed_analytics",
            "is_premium": False,
            "platform": "weba",
            "locale": "en",
            "client_timestamp": str(int(time.time() * 1000)),
            "Content": dynamic_content
        },
        {
            "event_name": "app-init",
            "session_id": "09e3e16f-a05f-45fd-8d80-4f5fd4d804f5",
            "user_id": 6973178056,
            "app_name": "seed_analytics",
            "is_premium": False,
            "platform": "weba",
            "locale": "en",
            "client_timestamp": str(int(time.time() * 1000)),
            "Content": dynamic_content
        }
    ]

    headers = {
        'Content-Type': 'application/json',
        'tga-auth-token': 'YOUR_ACTUAL_TOKEN_HERE',
    }


    full_url = f'https://tganalytics.xyz{dynamic_url_suffix}'
    response = requests.post(full_url, headers=headers, json=payload)

    if response.status_code in [204, 201, 202]:
        access_token = response.headers.get('tga-auth-token')
        expires_in = time.time() + 3600
    else:
        print(f"[ ERROR ]: Gagal memperbarui token, status code: {response.status_code}")
        print(f"Response: {response.text}")

def ensure_token():
    global access_token, expires_in

    if access_token is None or time.time() >= expires_in:
        refresh_token()

def get_profile():
    ensure_token()  # Pastikan token aktif
    headers['Authorization'] = f'Bearer {access_token}'
    response = requests.get(url_get_profile, headers=headers)
    if response.status_code == 200:
        profile_data = response.json()
        name = profile_data['data']['name']
        print(f"{Fore.CYAN + Style.BRIGHT}============== [ Akun | {name} ] ==============")
    else:
        print(f"{Fore.RED + '[ Profile ]: Gagal mendapatkan data, status code: {response.status_code}'}")

def check_worm():
    response = requests.get('https://elb.seeddao.org/api/v1/worms', headers=headers)
    if response.status_code == 200:
        worm_data = response.json()['data']
        next_refresh = worm_data['next_worm']
        is_caught = worm_data['is_caught']
        next_refresh_dt = datetime.datetime.fromisoformat(next_refresh[:-1] + '+00:00')
        now_utc = datetime.datetime.now(pytz.utc)
        time_diff_seconds = (next_refresh_dt - now_utc).total_seconds()
        hours = int(time_diff_seconds // 3600)
        minutes = int((time_diff_seconds % 3600) // 60)
        print(f"{Fore.GREEN + Style.BRIGHT}[ Worms ]: Next in {hours} jam {minutes} menit - Status: {'Caught' if is_caught else 'Available'}")
        return worm_data
    else:
        print(f"{Fore.RED + Style.BRIGHT}[ Worms ]: Gagal mendapatkan data worm.")
        return None

def catch_worm():
    worm_data = check_worm()
    if worm_data and not worm_data['is_caught']:
        response = requests.post('https://elb.seeddao.org/api/v1/worms/catch', headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Berhasil menangkap")
            #
        elif response.status_code == 400:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Sudah terangkap")
        elif response.status_code == 404:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Worm tidak ditemukan")    
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Gagal menangkap worm, status code:", response)
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Cacing Sudah di Tangkap, Tanggkap 🐷 dulu")

def get_profile():
    response = requests.get(url_get_profile, headers=headers)
    if response.status_code == 200:
        profile_data = response.json()
        name = profile_data['data']['name']
        print(f"{Fore.CYAN + Style.BRIGHT}============== [ Akun | {name} ] ==============")
        upgrades = {}
        for upgrade in profile_data['data']['upgrades']:
            upgrade_type = upgrade['upgrade_type']
            upgrade_level = upgrade['upgrade_level']
            upgrades[upgrade_type] = max(upgrade_level, upgrades.get(upgrade_type, 0))
        for upgrade_type, level in upgrades.items():
            print(f"{Fore.BLUE + Style.BRIGHT}[ {upgrade_type.capitalize()} Level ]: {level + 1}")
    else:
        print(f"{Fore.RED + '[ Profile ]: Gagal mendapatkan data, status code: {response.status_code}'}")

def check_balance():
    response = requests.get(url_balance, headers=headers)
    if response.status_code == 200:
        balance_data = response.json()
        print(f"{Fore.YELLOW + Style.BRIGHT}[ Balance ]: {balance_data['data'] / 1000000000}")
        return True
    else:
        print(f"{Fore.RED + Style.BRIGHT}[ Balance ]: Gagal | {response.status_code}")
        return False

def cekin_daily():
    response = requests.post(url_checkin, headers=headers)
    if response.status_code == 200:
        day = response.json().get('data', {}).get('no', '')
        print(f"{Fore.GREEN + Style.BRIGHT}[ Check-in ]: Check-in berhasil | Day {day}")
    else:
        data = response.json()
        if data.get('message') == 'already claimed for today':
            print(f"{Fore.RED + Style.BRIGHT}[ Check-in ]: Sudah dilakukan hari ini")
        else:
            print(f"{Fore.RED + Style.BRIGHT}[ Check-in ]: Gagal | {data}")

def upgrade_storage(confirm):
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_storage, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade storage ]: Berhasil'
        else:
            return '[ Upgrade storage ]: Balance tidak tercukupi'
    else:
        return None

def upgrade_mining(confirm):
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_mining, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade mining ]: Berhasil'
        else:
            return '[ Upgrade mining ]: Balance tidak tercukupi'
    else:
        return None

def upgrade_holy(confirm):
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_holy, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade holy ]: Berhasil'
        else:
            return '[ Upgrade holy ]: Syarat tidak terpenuhi'
    else:
        return None

def get_tasks():
    response = requests.get('https://elb.seeddao.org/api/v1/tasks/progresses', headers=headers)
    tasks = response.json()['data']
    for task in tasks:
        if task['task_user'] is None or not task['task_user']['completed']:
            complete_task(task['id'], task['name'])

def complete_task(task_id, task_name):
    response = requests.post(f'https://elb.seeddao.org/api/v1/tasks/{task_id}', headers=headers)
    if response.status_code == 200:
        print(f"{Fore.GREEN + Style.BRIGHT}[ Tasks ]: Tugas {task_name} selesai.")
    else:
        print(f"{Fore.RED + Style.BRIGHT}[ Tasks ]: Gagal menyelesaikan tugas {task_name}, status code: {response.status_code}")

def main():
    print_welcome_message()
    tokens = load_credentials()
    confirm_storage = input(Fore.BLUE + Style.BRIGHT + "Auto upgrade storage? (y/n): ")
    confirm_mining = input(Fore.WHITE + Style.BRIGHT + "Auto upgrade mining? (y/n): ")
    confirm_holy = input(Fore.CYAN + Style.BRIGHT + "Auto upgrade holy? (y/n): ")
    confirm_task = input(Fore.GREEN + Style.BRIGHT + "Auto Clear Task? (y/n): ")

    while True:
        ensure_token()
        hasil_upgrade = upgrade_storage(confirm_storage)
        hasil_upgrade1 = upgrade_mining(confirm_mining)
        hasil_upgrade2 = upgrade_holy(confirm_holy)

        for index, token in enumerate(tokens):
            headers['telegram-data'] = token
            info = get_profile()
            if info:
                print(f"Memproses untuk token ke {info['data']['name']}")

            if hasil_upgrade:
                print(hasil_upgrade)
                time.sleep(1)
            if hasil_upgrade1:
                print(hasil_upgrade1)
                time.sleep(1)
            if hasil_upgrade2:
                print(hasil_upgrade2)
                time.sleep(1)
            if check_balance():
                response = requests.post(url_claim, headers=headers)
                if response.status_code == 200:
                    print(f"{Fore.GREEN + Style.BRIGHT}[ Claim ]: Claim berhasil")
                elif response.status_code == 400:

                    response_data = response.json()
                    print(f"{Fore.RED + Style.BRIGHT}[ Claim ]: Belum waktunya claim")
                else:
                    print("Terjadi kesalahan, status code:", response.status_code)

                cekin_daily()
                catch_worm()
                if confirm_task.lower() == 'y':
                    get_tasks()

        for i in range(30, 0, -1):
            sys.stdout.write(f"\r{Fore.CYAN + Style.BRIGHT}============ Selesai, tunggu {i} detik.. ============")
            sys.stdout.flush()
            time.sleep(1)
        print()
        clear_console()

if __name__ == "__main__":
    main()
