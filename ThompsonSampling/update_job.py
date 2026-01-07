# update_job.py
import json
from thompson_sampler import ThompsonDataSampler

dummy_data = json.load(open("train.json", encoding="utf-8"))
sampler = ThompsonDataSampler(dummy_data,
                              state_path="state.json",
                              auto_load=True)

stats = json.load(open("dev_stats_1.json", encoding="utf-8"))   
sampler.update_posterior(stats)            
