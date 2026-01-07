
export WANDB_MODE=offline
# export SWANLAB_MODE="offline"

export CUDA_VISIBLE_DEVICES=0,1
accelerate launch \
    --num_processes 2 \
    --config_file=recipes/accelerate_configs/zero3.yaml src/open_r1/sft.py \
    --model_name_or_path Qwen2.5-7B-Instruct \
    --dataset_name CMR-R/cardiac_sft_json_mode.jsonl \
    --dataset_config "" \
    --eos_token '<|im_end|>' \
    --learning_rate 4.0e-5 \
    --num_train_epochs 3 \
    --max_seq_length 8192 \
    --per_device_train_batch_size 2 \
    --gradient_checkpointing \
    --bf16 \
    --logging_strategy="steps"\
    --logging_steps=1\
    --use_liger_kernel \
    --output_dir data/Cardiac_sft \
    --save_strategy steps \
    --save_steps 5000

