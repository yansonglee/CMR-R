export WANDB_MODE=offline
CUDA_VISIBLE_DEVICES=1,2,3 ACCELERATE_LOG_LEVEL=info \
    accelerate launch \
    --num_processes 3\
    --config_file recipes/accelerate_configs/zero3.yaml \
    src/open_r1/grpo.py --config recipes/Qwen2.5-7B-Instruct/grpo/config_demo.yaml \
    --vllm_mode server


