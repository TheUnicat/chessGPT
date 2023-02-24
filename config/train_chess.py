# train a miniature character-level shakespeare model
# good for debugging and playing on macbooks and such

out_dir = 'out-chessGPT-char'
eval_interval = 2000 # keep frequent because we'll overfit
eval_iters = 200
log_interval = 10 # don't print too too often

# we expect to overfit on this small dataset, so only save when val improves
always_save_checkpoint = False

wandb_log = False # override via command line if you like
wandb_project = 'shakespeare-char'
wandb_run_name = 'mini-gpt'

dataset = 'chess'
batch_size = 32
block_size = 512 # context of up to 256 previous characters

# baby GPT model :)
n_layer = 16
n_head = 32
n_embd = 512
dropout = 0.2

learning_rate = 6e-5 # with baby networks can afford to go a bit higher
max_iters = 500000
lr_decay_iters = 40000  # make equal to max_iters usually
min_lr = 5e-6 # learning_rate / 10 usually
beta2 = 0.99 # make a bit bigger because number of tokens per iter is small

warmup_iters = 100 # not super necessary potentially
#compile = True
# on macbook also add
# device = 'cpu'  # run on cpu only
# compile = False # do not torch compile the model
