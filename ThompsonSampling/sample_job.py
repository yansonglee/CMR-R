# sample_job.py
import json, os
from thompson_sampler import ThompsonDataSampler

data = json.load(open("train.json", encoding="utf-8"))

sampler = ThompsonDataSampler(data,
                              batch_size=2000,
                              small_threshold=2000,
                              seed=2024,
                              state_path="state.json",
                              auto_load=True)    

subset, json_file = sampler.sample_once(save_dir="samples")
