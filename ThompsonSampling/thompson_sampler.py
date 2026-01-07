# thompson_sampler.py
# -*- coding: utf-8 -*-
import json, random, math, datetime, os
from collections import defaultdict
from typing import Dict, List, Tuple

class ThompsonDataSampler:
    
    def __init__(self,
                 data: List[dict],
                 batch_size: int = 256,
                 small_threshold: int = 100,
                 seed: int = 42,
                 state_path: str = "state.json",
                 auto_load: bool = True):
        
        self.batch_size = batch_size
        self.small_threshold = small_threshold
        self.rng = random.Random(seed)
        self.state_path = state_path

        if auto_load and os.path.exists(state_path):
            self._load_state(state_path)
            print(f"[Init] state loaded from {state_path}, stage={self.stage_id}")
        else:
           
            self.pool = defaultdict(list)           # {label: [...]}
            for row in data:
                self.pool[row["label"]].append(row)

            # Beta(1,1)
            self.alpha = {c: 1.0 for c in self.pool}
            self.beta  = {c: 1.0 for c in self.pool}
            self.stage_id = 0
            self._save_state()                      

   
    def sample_once(self, save_dir="samples", autosave=True):
        os.makedirs(save_dir, exist_ok=True)
        self.stage_id += 1
      
        weight = {c: 1.0 - self.rng.betavariate(self.alpha[c], self.beta[c])
                  for c in self.pool}
        tot_w = sum(weight.values()) or len(weight)
        
        quota = {c: int(round(weight[c] / tot_w * self.batch_size))
                 for c in weight}
        selected, deficit = [], 0
        
        for c, need in quota.items():
            if need == 0:
                continue
            pool_list = self.pool[c]
            remain = len(pool_list)
            if remain < self.small_threshold:  
                take_n = min(need, remain)  
                if take_n:
                    idx = self.rng.sample(range(remain), take_n)
                    selected.extend(pool_list[i] for i in idx)
                deficit += need - take_n 
             
                continue
            
            if remain <= need:  
                selected.extend(pool_list)
                pool_list.clear()
                deficit += need - remain
            else:  
                idx = self.rng.sample(range(remain), need)
                for i in sorted(idx, reverse=True):
                    selected.append(pool_list[i])
                    pool_list.pop(i)
       
        for _ in range(deficit):
            big_candidates = [c for c in self.pool if len(self.pool[c]) > 0]
            if not big_candidates:  
                break
            c = self.rng.choice(big_candidates)
            pool_list = self.pool[c]
            j = self.rng.randrange(len(pool_list))
            selected.append(pool_list.pop(j))
      
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        fname = os.path.join(save_dir, f"stage{self.stage_id}_{ts}.json")
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(selected, f, ensure_ascii=False, indent=2)
        if autosave:
            self._save_state()
        print(f"[Stage {self.stage_id}] sampled {len(selected)} rows → {fname}")
        return selected, fname

    def update_posterior(self,
                         acc_info: Dict[str, Tuple[int, int]],
                         autosave: bool = True):
        """
        acc_info : {"labelA": (correct_cnt, total_cnt), ...}
        """
        for c, (correct, total) in acc_info.items():
        
            if c not in self.alpha:
                self.alpha[c] = 1.0
                self.beta[c]  = 1.0
            self.alpha[c] += correct
            self.beta[c]  += (total - correct)

        if autosave:
            self._save_state()
        print(f"[Update] posterior updated for {len(acc_info)} classes.")

    
    def _save_state(self, path: str = None):
        path = path or self.state_path
        state = {
            "pool": self.pool,        # defaultdict(list)
            "alpha": self.alpha,
            "beta":  self.beta,
            "stage_id": self.stage_id,
        }

        state["pool"] = {k: v for k, v in state["pool"].items()}
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        # print(f"[Save] state saved to {path}")

    def _load_state(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            state = json.load(f)
        self.pool = defaultdict(list, {k: v for k, v in state["pool"].items()})
        self.alpha = state["alpha"]
        self.beta  = state["beta"]
        self.stage_id = state["stage_id"]
