import requests
import json
from datetime import datetime


class AlephiumMiner:
    def __init__(self, address):
        self.address = address
        self.base_url = "https://alephium.herominers.com/api"
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "alephium.herominers.com",
            "Referer": "https://alephium.herominers.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.headers["Cookie"] = f"mining_address={self.address}"

    def get_stats(self, recent_blocks_amount=20, longpoll=False):
        url = f"{self.base_url}/stats_address"
        params = {
            "address": self.address,
            "recentBlocksAmount": str(recent_blocks_amount),
            "longpoll": str(longpoll).lower()
        }
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            self.data = json.loads(response.text)
            return response.json()
        else:
            raise Exception(f"Error fetching stats: {response.status_code}")

    def save_stats_to_file(self, data, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"alephium_stats_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Stats saved to {filename}")

    def update_data(self):
        # Здесь должен быть код для получения данных с API
        # Для примера используем данные из предоставленного JSON
        with open('paste.txt', 'r') as file:
            self.data = json.load(file)

    def hashrate_to_gh(self, hashrate):
        return hashrate / 1e9

    def get_total_hashrate(self):
        if not self.data:
            self.get_stats()
        return self.hashrate_to_gh(self.data['stats']['hashrate'])

    def get_hashrate_1h(self):
        if not self.data:
            self.get_stats()
        return self.hashrate_to_gh(self.data['stats']['hashrate_1h'])

    def get_hashrate_6h(self):
        if not self.data:
            self.get_stats()
        return self.hashrate_to_gh(self.data['stats']['hashrate_6h'])

    def get_hashrate_24h(self):
        if not self.data:
            self.get_stats()
        return self.hashrate_to_gh(self.data['stats']['hashrate_24h'])

    def get_workers_info(self):
        if not self.data:
            self.update_data()
        workers_info = []
        for worker in self.data['workers']:
            workers_info.append({
                'name': worker['name'],
                'hashrate_gh': self.hashrate_to_gh(worker['hashrate']),
                'hashrate_1h_gh': self.hashrate_to_gh(worker['hashrate_1h']),
                'hashrate_6h_gh': self.hashrate_to_gh(worker['hashrate_6h']),
                'hashrate_24h_gh': self.hashrate_to_gh(worker['hashrate_24h'])
            })
        return workers_info

    def print_summary(self):
        print(f"Общий хешрейт: {self.get_total_hashrate():.2f} GH/s")
        print(f"Хешрейт за последний час: {self.get_hashrate_1h():.2f} GH/s")
        print(
            f"Хешрейт за последние 6 часов: {self.get_hashrate_6h():.2f} GH/s")
        print(
            f"Хешрейт за последние 24 часа: {self.get_hashrate_24h():.2f} GH/s")

        print("\nИнформация о воркерах:")
        for worker in self.get_workers_info():
            print(f"Имя: {worker['name']}")
            print(f"  Текущий хешрейт: {worker['hashrate_gh']:.2f} GH/s")
            print(f"  Хешрейт за 1 час: {worker['hashrate_1h_gh']:.2f} GH/s")
            print(f"  Хешрейт за 6 часов: {worker['hashrate_6h_gh']:.2f} GH/s")
            print(f"  Хешрейт за 24 часа: {worker['hashrate_24h_gh']:.2f} GH/s")
            print()
