from herominers import AlephiumMiner

miner = AlephiumMiner("1JE6caq2WcKP97XUNesoie1KpYd4Jj5Tixs7HXKKCsKD3")
miner.get_stats()
print(miner.get_total_hashrate())
miner.print_summary()