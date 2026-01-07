# CMR-R: Explicit Chain of Diagnosis for CMR Semantic Interpretation via Large Reasoning Model 🫀🧠



**CMR-R** (Cardiac Magnetic Resonance - Reasoning) is a specialized Large Reasoning Model (LRM) designed to provide an **Explicit Chain of Diagnosis (CoD)** for cardiovascular diseases.

Unlike traditional "black-box" AI models, CMR-R not only outputs a diagnosis but also generates a transparent reasoning pathway derived from CMR semantic features and functional parameters. It achieves diagnostic accuracy surpassing experienced radiologists (>10 years of experience) and leading general LLMs (e.g., GPT-5, DeepSeek-V3).

---

## 🌟 Key Features

* **Explicit Chain of Diagnosis (CoD):** Simulates the reasoning process of clinical experts, providing step-by-step evidence from imaging features to pathological conclusions.
* **State-of-the-Art Performance:** Achieved **ACC: 0.858** and **AUC: 0.944** across 8 cardiac categories, outperforming radiologists and closed-source models.
* **Handle Long-Tail Diseases:** Significantly improved detection of rare diseases (e.g., Myocarditis, Amyloidosis) using **MA-GRPO** (Multi-stage Adaptive Group Relative Policy Optimization).
* **Prospective Continuous Learning:** Capable of evolving with unlabeled, noisy prospective data via **PCRL** (Prospective Continuous Reinforcement Learning).
