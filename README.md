# chessGPT
A chess engine built on the decision transformer architecture.
Start by moving the directory into your Documents folder. Navigate to the command line and type

cd Documents/chessGPT

...and hit enter.
To train a chessGPT model (add data to data/chess before doing this), simply type 

python3 train.py config/train_chess.py --init_from=resume --device=cuda --max_iters=100000

...into the command line if you have a GPU. If you only have a MacBook, or other personal computer, replace "cuda" with "cpu" or "mps" (on MacBook).
This is strongly discouraged as it will take an extremely long time to train the model to even play legal moves.

Do NOT torch.compile model, it will fail :(

Dependencies:

PyTorch (1.13.1 is preferred)
NumPy
python-chess

To play chess against the engine, move the ckpt.pt file to out-chessGPT-char (if it isn't there already) and then type

python3 test_against_engine.py

...into your terminal. This should create an emoji-based chessboard (utf supported!)
You'll play white (for really complicated reasons relating to how I completely botched creating the training data, it's not possible to play as black) and
the computer should reply within ~5-10 seconds, even on cpu. 

The engine was trained on a sanitized dataset of 500k human chess games. ChessGPT is not a strong chess engine by modern standards, but it will (usually)
capture hanging pieces! It suffers from significant overfitting problems in the early game and will often make mistakes if confronted with offbeat 
opening lines. Generating trajectories is a two-step process. The model first "self-prompts" the returns-to-go (i.e. moves until game end) from the
current state and a condition of victory. The reward is then combined with the last n board & move encodings (default 3) to generate the next action.
