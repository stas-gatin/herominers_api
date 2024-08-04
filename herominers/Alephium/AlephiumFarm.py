import requests
import json
from datetime import datetime


class AlephiumFarm:
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
        self.data = self.update_stats()

    def update_stats(self, recent_blocks_amount=20, longpoll=False):
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

    def save_stats_to_file(self, filename=None):
        data = self.update_stats()
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"alephium_stats_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Stats saved to {filename}")

    @staticmethod
    def hashrate_to_gh(hashrate):
        return hashrate / 1e9

    def farm_total_hashrate(self):
        return self.hashrate_to_gh(self.data['stats']['hashrate'])

    def farm_hashrate_1h(self):
        return self.hashrate_to_gh(self.data['stats']['hashrate_1h'])

    def farm_hashrate_6h(self):
        return self.hashrate_to_gh(self.data['stats']['hashrate_6h'])

    def farm_hashrate_24h(self):
        return self.hashrate_to_gh(self.data['stats']['hashrate_24h'])

    def farm_shares_good(self):
        return self.data['stats']['shares_good']

    def farm_shares_invalid(self):
        return self.data['stats']['shares_invalid']

    def farm_shares_stale(self):
        return self.data['stats']['shares_stale']

    def farm_blocks_found(self):
        return self.data['stats']['blocksFound']

    def worker_total_hashrate(self):
        return self.hashrate_to_gh(self.data['worker']['hashrate'])

    def worker_hashrate_1h(self):
        return self.hashrate_to_gh(self.data['worker']['hashrate_1h'])

    def worker_hashrate_6h(self):
        return self.hashrate_to_gh(self.data['worker']['hashrate_6h'])

    def worker_hashrate_24h(self):
        return self.hashrate_to_gh(self.data['worker']['hashrate_24h'])

    def worker_shares_good(self):
        return self.data['worker']['shares_good']

    def worker_shares_invalid(self):
        return self.data['worker']['shares_invalid']

    def worker_shares_stale(self):
        return self.data['worker']['shares_stale']

    def dead_workers(self):
        workers = []
        for worker in self.data['workers']:
            if worker['hashrate'] == 0:
                workers.append(worker["name"])
        return workers

    def online_workers(self):
        workers = []
        for worker in self.data['workers']:
            if worker['hashrate'] != 0:
                workers.append(worker["name"])
        return workers

    def get_workers_stats(self):
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

    def get_worker_stats(self, worker_name: str):
        for worker in self.data['workers']:
            if worker['name'] == worker_name:
                return {
                    'name': worker['name'],
                    'hashrate_gh': self.hashrate_to_gh(worker['hashrate']),
                    'hashrate_1h_gh': self.hashrate_to_gh(worker['hashrate_1h']),
                    'hashrate_6h_gh': self.hashrate_to_gh(worker['hashrate_6h']),
                    'hashrate_24h_gh': self.hashrate_to_gh(worker['hashrate_24h'])
                }
