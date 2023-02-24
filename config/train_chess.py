# train chessGPT based on your dataset
# default values, can be overridden in command line based on your hardware and preferences

out_dir = 'out-chessGPT-char'
eval_interval = 2000 # keep infrequent because training will take a long time
eval_iters = 200
log_interval = 10 # don't print too too often

# Learning can happen even if loss does not go down
# Downstream performance can increase despite loss not decreasing
always_save_checkpoint = True

wandb_log = False # Please don't do this

dataset = 'chess'
batch_size = 16
block_size = 512 # context of up to 256 previous characters

# chessGPT :)
n_layer = 16
n_head = 32
n_embd = 512
dropout = 0.2

learning_rate = 6e-4 # learning rate can be higher with medium-sized (~50M parameters for chessGPT) networks
max_iters = 100000 # Adjust based on your preferences
lr_decay_iters = 100000  # Cosine learning decay is used, so keep it equal to max_iters
min_lr = 6e-5 # learning_rate / 10 usually
beta2 = 0.99 # make a bit bigger because number of tokens per iter is small

warmup_iters = 1000 # keep this
compile = False # only change if you've fixed the problems with this

