# chessGPT
A chess engine built on the decision transformer architecture. Built on the nanoGPT repository made by Andrej Karpathy.

Currently working on a second version with pretraining on randomly-generated trajectories to reduce overfitting.


QUICK START:

Just move model file (ckpt.pt) to out-chessGPT-char and run

cd chessGPT
python3 play.py

...and a chessboard should pop out of the terminal.

Extended instructions:

python installation:

Go to python.org and install python.
Go to the command line or terminal (depending on os) and download repositories by typing the below commands into the shell, one-by-one:


pip install torch

pip install numpy

pip install chess

(Try "pip3" on macOS or if pip fails)


Next, download this repository by clicking the green 'Code' button on the main page of the repository, followed by 'local'. Click 'Download ZIP'.
Unzip file.

Start by moving the directory into your Documents folder. Navigate to the command line and type

cd Documents/chessGPT

...and hit enter.

Training:

skip training step if you have model file (ckpt.pt file) in the path chessGPT/out-chessGPT-char/ckpt.pt. Jump to the 'sampling' section.

To train a chessGPT model (add data to data/chess before doing this), simply type 

python3 train.py config/train_chess.py --init_from=scratch --device=cuda --max_iters=100000

...into the command line if you have a GPU. If you only have a MacBook, or other personal computer, replace "cuda" with "cpu" or "mps" (on MacBook).
This is strongly discouraged as it will take an extremely long time to train the model to even play legal moves. A minimum of one GPU is recommended,
preferably at least 2 V100s or A100s.

Do NOT torch.compile model, it will fail :(

Dependencies:


PyTorch (1.13.1 is preferred)

NumPy

python-chess


Sampling:

To play chess against the engine, move the ckpt.pt file to out-chessGPT-char (if it isn't there already) and then type

python3 play.py

...into your terminal. This should create an emoji-based chessboard (utf supported!)
You'll play white (for really complicated factors relating to how I completely botched creating the training data, it's not possible to play as black) and
the computer should reply within ~5-10 seconds, even on cpu. 

The engine was trained on a sanitized dataset of 500k human chess games. ChessGPT is not a strong chess engine by modern standards, but it will (usually)
capture hanging pieces! It suffers from significant overfitting problems in the early game and will often make mistakes if confronted with offbeat 
opening lines. Generating trajectories is a two-step process. The model first "self-prompts" the returns-to-go (i.e. moves until game end) from the
current state and a condition of victory. The reward is then combined with the last n board & move encodings (default 3) to generate the next action.


TODOs:

-Bundle cleanser_chess.py sanitization functions into one function

-Edit training script to be compatible with torch.compile and PyTorch Nightly

-Allow command line arguments for context length and temperature when sampling

-Build v2 with pretraining on a corpus of randomly-generated chess games followed by finetuning on expert games

-Write function for evaluating against stockfish
