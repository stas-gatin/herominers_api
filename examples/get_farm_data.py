from herominers import AlephiumFarm


def print_summary(farm: AlephiumFarm):
    print(f"Total hashrate: {farm.farm_total_hashrate():.2f} GH/s")
    print(f"Hashrate in the last hour: {farm.farm_hashrate_1h():.2f} GH/s")
    print(
        f"Hashrate in the last 6 hours: {farm.farm_hashrate_6h():.2f} GH/s")
    print(
        f"Hashrate in the last 24 hours: {farm.farm_hashrate_24h():.2f} GH/s")

    print("\nWorker information:")
    for worker in farm.get_workers_stats():
        print(f"Name: {worker['name']}")
        print(f"  Current hashrate: {worker['hashrate_gh']:.2f} GH/s")
        print(
            f"  Hashrate over 1 hour: {worker['hashrate_1h_gh']:.2f} GH/s")
        print(
            f"  Hashrate over 6 hours: {worker['hashrate_6h_gh']:.2f} GH/s")
        print(
            f"  Hashrate over 24 hours: {worker['hashrate_24h_gh']:.2f} GH/s")
        print()


if __name__ == "__main__":
    alephium_farm = AlephiumFarm(
        "1JE6caq2WcKP97XUNesoie1KpYd4Jj5Tixs7HXKKCsKD3"
    )
    print_summary(alephium_farm)
