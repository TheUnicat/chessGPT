import chess
import chess.engine
import time
import os
import chess.svg
import re
import random
import contextlib
"""
Sample from a trained model
"""

import pickle
from contextlib import nullcontext
import torch
import tiktoken
from model import GPTConfig, GPT
import random

def prompt_gpt(prompt, new_tokens, compiley, devicey, home, modele=False):
    # -----------------------------------------------------------------------------
    init_from = 'resume' # either 'resume' (from an out_dir) or a gpt2 variant (e.g. 'gpt2-xl')
    out_dir = 'out-chessGPT-char' # ignored if init_from is not 'resume'
    start = prompt # or "<|endoftext|>" or etc. Can also specify a file, use as: "FILE:prompt.txt"
    num_samples = 1 # number of samples to draw
    max_new_tokens = new_tokens # number of tokens generated in each sample
    temperature = 1 # 1.0 = no change, < 1.0 = less random, > 1.0 = more random, in predictions
    top_k = 200 # retain only the top_k most likely tokens, clamp others to have 0 probability
    seed = random.randint(1, 10000)
    device = devicey # examples: 'cpu', 'cuda', 'cuda:0', 'cuda:1', etc.
    dtype = 'bfloat16' # 'float32' or 'bfloat16' or 'float16'
    compile = compiley # use PyTorch 2.0 to compile the model to be faster
    #exec(open('configurator.py').read()) # overrides from command line or config file
    # -----------------------------------------------------------------------------
    compile = False
    device = "cpu"
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cuda.matmul.allow_tf32 = True # allow tf32 on matmul
    torch.backends.cudnn.allow_tf32 = True # allow tf32 on cudnn
    device_type = 'cuda' if 'cuda' in device else 'cpu' # for later use in torch.autocast
    ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
    ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)

    # model
    # init from a model saved in a specific directory
    if modele == False:
        if home:
            ckpt_path = os.path.join(out_dir, 'ckpt.pt')
        else:
            ckpt_path = os.path.join(out_dir, 'ckpt.pt')
        checkpoint = torch.load(ckpt_path, map_location=device)
        gptconf = GPTConfig(**checkpoint['model_args'])
        model = GPT(gptconf)
        state_dict = checkpoint['model']
        unwanted_prefix = '_orig_mod.'
        for k,v in list(state_dict.items()):
            if k.startswith(unwanted_prefix):
                state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
        model.load_state_dict(state_dict)
    else:
        model = modele


    model.eval()
    model.to(device)

        #print(f"Loading meta from {meta_path}...")
    with open("data/chess/meta.pkl", 'rb') as f:
        meta = pickle.load(f)
        # TODO want to make this more general to arbitrary encoder/decoder schemes
    stoi, itos = meta['stoi'], meta['itos']
    encode = lambda s: [stoi[c] for c in s]
    decode = lambda l: ''.join([itos[i] for i in l])


    # encode the beginning of the prompt
    if start.startswith('FILE:'):
        with open(start[5:], 'r', encoding='utf-8') as f:
            start = f.read()
    start_ids = encode(start)
    x = (torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...])

    # run generation
    with torch.no_grad():
        with ctx:
            for k in range(num_samples):
                y = model.generate(x, max_new_tokens, temperature=temperature, top_k=top_k)

                return decode(y[0].tolist())












def strip_unfinished():
    game = 0
    with open("individual_chess.txt", "r") as processed_file, open("processed_chess.txt", "w") as individual_file:
        new_line = "" # initialize an empty string to store each game
        for line in processed_file:
            game += 1
            if game %  10000 == 0:
                print(f'{game/10000} ten thousand lines done!')
            # if the line starts with "[[[[[", this means it is a result line and a new game is starting
            if line.startswith("[[[[[*"):
                continue
            else:
                individual_file.write(line)
                # if it is not a result line, remove the newline characters and add the line to new_line

#result, last_move = sanitizere(input_file, output_file)
#cleaner()
def pad_string(s):
    while len(s) < 4:
        s = '[' + s
    return s

def algebraic_to_coord(move, board):
    # Create a dictionary to convert file letters to numbers
    files = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

    # Parse the move using the chess library
    move = board.move_stack[-1]

    # Get the starting and ending squares of the move
    start = move.from_square
    end = move.to_square

    # Convert the squares to coordinates
    start_square = str(files[chess.square_name(start)[0]]) + str(chess.square_rank(start))
    end_square = str(files[chess.square_name(end)[0]]) + str(chess.square_rank(end))

    # Check if there's a promotion
    if move.promotion is not None:
        promotion = chess.piece_name(move.promotion)
        return start_square + end_square + promotion
    else:
        return start_square + end_square + 'M'
def parse_and_edit_string(input_str, value):
    #print(input_str)
    if input_str == "":
        print("HELP!!!!")
    if input_str == "":
        board = chess.Board()
        return "W" + board_encoding(board) + "H" + pad_string(value)
    substrings = [substr for substr in re.findall(r"[HX,].{4}", input_str) if substr[0] in ['H', 'X', ',']]
    #print(substrings)
    if len(substrings) == 0:
        output_string = input_str + ("H" + pad_string(value))
        #print(output_string)
        return output_string
    new_strings = []
    substrings.append('H' + pad_string(value))
    for i in substrings:
        new_strings.append("H" + pad_string(str(int(value) + (len(substrings) - (substrings.index(i) + 1)))))
    final_value = new_strings[-1]
    #print(new_strings)
    new_strings.pop(-1)
    #print("hi!")
    output_str = ''
    i = 0
    #print(new_strings)
    while i < len(input_str):
        if input_str[i] in ['H', 'X', ','] and i + 5 < len(input_str):
            output_str += new_strings[0]
            new_strings.pop(0)
            i += 5
        else:
            output_str += input_str[i]
            i += 1
    output_str += ("H" + pad_string(value))
    #print(output_str)
    return output_str

#parse_and_edit_string("Wrnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNRYYYYH[[35Wrnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNRYYYYH[[34Wrnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNRYYYY", "20")
def board_encoding(board, black=False):
    encoding = ""
    if black == False:
        for square in chess.SQUARES_180:
            piece = board.piece_at(square)
            if piece is not None:
                encoding += piece.symbol()
            else:
                encoding += '-'
    else:
        for square in chess.SQUARES_180:
            piece = board.piece_at(square)
            if piece is not None:
                encoding = piece.symbol() + encoding
            else:
                encoding = '-' + encoding
    if board.has_kingside_castling_rights(chess.WHITE):
        encoding += 'Y'
    else:
        encoding += '.'
    if board.has_queenside_castling_rights(chess.WHITE):
        encoding += 'Y'
    else:
        encoding += '.'
    if board.has_kingside_castling_rights(chess.BLACK):
        encoding += 'Y'
    else:
        encoding += '.'
    if board.has_queenside_castling_rights(chess.BLACK):
        encoding += 'Y'
    else:
        encoding += '.'
    return encoding
def decode_to_move(input_string, output_string):
    files = {1: 'a', 2: 'b', 3: 'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h'}
    try:
        output_string = output_string[len(input_string):]
        for char in output_string:
            if char == "w" or char == "W":
                move = output_string[(output_string.index(char) - 5):(output_string.index(char))]
                from_square = move[:2]
                to_square = move[2:4]
                promotion = move[-1]
                for value in move[:-1]:
                    try:
                        if (move.index(value) + 1) % 2 == 0:
                            if int(value) not in range(0, 8):
                                return False, "illegal"
                        elif int(value) not in range(1, 9):
                            return False, "illegal"
                    except:
                        return False, "illegal"
                decoded_move = ""
                decoded_move += str(files[int(from_square[0])])
                decoded_move += str(int(from_square[1]) + 1)
                decoded_move += str(files[int(to_square[0])])
                decoded_move += str(int(to_square[1]) + 1)
                if promotion != "M":
                    decoded_move += promotion
                return True, decoded_move
    except:
        return False, "illegal"
#decode_to_move("", "4047Mw")

def new_game_encoder(colour, reward, inputy, san=True, is_list=False):
    if 1 == 1:
        if 2 == 2:
            if 3 == 3:
                board = chess.Board()
                new_line = ""
                if not is_list:
                    moves = inputy.split(" ")
                    for move in moves:
                        if move == " " or move == "\n":
                            moves.pop(moves.index(move))
                else:
                    moves = inputy
                #print(result)
                # convert result to a scalar value
                #print(reward)
                if reward == ",":
                    if colour == 0:
                        move_side = 0
                        for move in moves:
                            if move_side == 0:
                                move_side = 1
                                new_line += pad_string(",")
                                try:
                                    if san==True:
                                        board.push_san(move)
                                    else:
                                        board.push(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "W"
                            else:
                                move_side = 0
                                try:
                                    if san==True:
                                        board.push_san(move)
                                    else:
                                        board.push(move)
                                    new_line += board_encoding(board)
                                except:
                                    new_line = ""
                                    break
                    else:
                        move_side = 0
                        for move in moves:
                            if move_side == 1:
                                move_side = 0
                                new_line += pad_string(",")
                                try:
                                    if san==True:
                                        board.push_san(move)
                                    else:
                                        board.push(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "w"
                            else:
                                move_side = 1
                                try:
                                    if san==True:
                                        board.push_san(move)
                                    else:
                                        board.push(move)
                                    new_line += board_encoding(board)
                                except:
                                    new_line = ""
                                    break
                        
                elif reward[0] == "H":
                    reward = int(float(reward[1:]))
                    if colour == 0:
                        move_side = 0
                        for move in moves:
                            if move_side == 0:
                                move_side = 1
                                new_line += "H"
                                new_line += str(reward)
                                reward += -1
                                try:
                                    if san==True:
                                        board.push_san(move)
                                    else:
                                        board.push(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "W"
                            else:
                                move_side = 0
                                try:
                                    if san==True:
                                        board.push_san(move)
                                    else:
                                        board.push(move)
                                    new_line += board_encoding(board)
                                except:
                                    print(move)
                                    print(board)
                                    new_line = ""
                                    break
                    else:
                        move_side = 0
                        for move in moves:
                            if move_side == 1:
                                move_side = 0
                                new_line += "H"
                                new_line += pad_string(str(reward))
                                reward += -1
                                try:
                                    if san==True:
                                        board.push_san(move)
                                    else:
                                        board.push(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "w"
                            else:
                                move_side = 1
                                try:
                                    if san==True:
                                        board.push_san(move)
                                    else:
                                        board.push(move)
                                    new_line += board_encoding(board)
                                except:
                                    new_line = ""
                                    break
                else:
                    reward = int(float(reward[1:]))
                    if colour == 0:
                        move_side = 0
                        for move in moves:
                            if move_side == 0:
                                move_side = 1
                                new_line += "X"
                                new_line += pad_string(str(reward))
                                reward += -1
                                try:
                                    board.push_san(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "W"
                            else:
                                move_side = 0
                                try:
                                    board.push_san(move)
                                    new_line += board_encoding(board)
                                except:
                                    new_line = ""
                                    break
                    else:
                        move_side = 0
                        for move in moves:
                            if move_side == 1:
                                move_side = 0
                                new_line += "X"
                                new_line += pad_string(str(reward))
                                reward += -1
                                try:
                                    if san==True:
                                        board.push_san(move)
                                    else:
                                        board.push(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "w"
                            else:
                                move_side = 1
                                try:
                                    if san==True:
                                        board.push_san(move)
                                    else:
                                        board.push(move)
                                    new_line += board_encoding(board)
                                except:
                                    new_line = ""
                                    break
    if len(new_line) >= 500:
        new_line = new_line[len(new_line) - 500:]
    return new_line
    #print(moves)
def comp_rewards(board, colour, compiley=False, devicey='cpu', home=True, model=False):
    encodings = board_encoding(board)
    if colour == 0:
        prompt = "W" + encodings + "H"
    elif colour == 1:
        prompt = "w" + encodings + "H"
    else:
        return False
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        reply = prompt_gpt(prompt, 4, compiley, devicey, home, model)
    return reply
   # return prompt_gpt(
#board = chess.Board()
#print(comp_rewards(board, 0, False, 'cpu', True)[-4:].strip("["))
def chessGPT(board, moves_list, colour, model=False):
    try:
        new_prompt_reward = comp_rewards(board, colour, model)[-4:].strip("[")
        print(new_prompt_reward)
        new_prompt = new_game_encoder(colour, "H100", moves_list, san=False, is_list=True)
        #print(new_prompt)
        new_prompt = parse_and_edit_string(new_prompt, str(new_prompt_reward))
        #print(new_prompt)
        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
            reply = prompt_gpt(new_prompt, 6, False, "cpu", True, model)
        #print(reply[-10:])
        try:
            reply = decode_to_move(new_prompt, reply)
            if not reply[0] == False:
                return reply[1]
            else:
                return False
        except:
            return False
    except:
        return False
def print_pos(pos):
    print()
    uni_pieces = {'r':'♜', 'n':'♞', 'b':'♝', 'q':'♛', 'k':'♚', 'p':'♟',
                  'R':'♖', 'N':'♘', 'B':'♗', 'Q':'♕', 'K':'♔', 'P':'♙', '.':'·'}
    counter = 0
    position_print = []
    for square in chess.SQUARES:
        if counter % 8 == 0:
            print("\n")
        counter += 1
        try:
            position_print.append(uni_pieces[pos.piece_at(square).symbol()])
            #position_print.append(pos.piece_at(square).symbol())
        except:
            position_print.append("*")
    while len(position_print) > 0:
        to_print = ""
        try:
            for i in range(8):
                to_print += position_print[-1]
                position_print.pop(-1)
        except:
            return
        to_printy = ""
        i = len(to_print) - 1
        while i >= 0:
            to_printy += (to_print[i])
            to_printy += " "
            i += -1
        print(to_printy)

def play_game(model = False):
    # Initialize the chess board and engine
    board = chess.Board()
    #engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    did_illegal = False
    # Choose the player's color randomly
    #player_color = chess.WHITE if bool(random.getrandbits(1)) else chess.BLACK

    # Initialize the moves list
    moves_list = []
    #comp_colour = 0 if player_color == chess.WHITE else 1
    #print(comp_colour)
    #comp_colour = 0
    #print(player_color)
    comp_colour = 1
    player_color = chess.BLACK
    # Play the game
    flag = False
    while not board.is_game_over():
        invalid_count = 0
        if board.turn == player_color:
            #print(board)
            print_pos(board)
            print("Board after engine move")
            # Get the player's move
            #print(movess)
            #for move in moves_list:
                #print(type(move))
            if model == False:
                try:
                    player_move = chessGPT(board, moves_list, comp_colour) # Replace with your own implementation
                    if player_move == False:
                        return len(moves_list), True, 0
                except:
                    return len(moves_list), True, 0
                
            else:
                flag = True
                try:
                    player_move = chessGPT(board, moves_list, comp_colour, model) # Replace with your own implementation
                    if player_move == False:
                        return len(moves_list), True, 0
                except:
                    return len(moves_list), True, 0
            # Make the move on the board
            moveyy = chess.Move.from_uci(player_move)
            #print(player_move)
            try:
                if moveyy in list(board.legal_moves):
                    board.push(moveyy)
                else:
                    return len(moves_list), True, 0
            except:
                did_illegal = True
                return len(moves_list), did_illegal, 0
            #print(board)
            moves_list.append(moveyy)
            #print(moves_list)
            # Add the move to the moves list
        else:
            print_pos(board)
            print("Board after chessGPT move")
            # Get the engine's move
            #time.sleep(1)
            #result = engine.play(board, chess.engine.Limit(time=1))
            engine_move = random.choice(list(board.legal_moves))
            #engine_move = result.move
            # Make the move on the board
            board.push(engine_move)
            #print(board)
            moves_list.append(engine_move)
            #print(moves_list)
            # Add the move to the moves list

    # Close the engine
    #engine.quit()
    if board.result() == "1-0":
        result = 0
    elif board.result() == "0-1":
        result = 1
    else:
        result = 0.5
    # Return the final board and moves list
    return len(moves_list), did_illegal, result

def metatest(num_games=10, model = False):
    total_illegals = 0
    total_moves = 0
    total_rewards = 0
    i = 0
    while i < num_games:
        if model == False:
            temp_length, temp_illegal, resulty = play_game()
        else:
            temp_length, temp_illegal, resulty = play_game(model)
        total_moves += int(temp_length / 2)
        if temp_illegal == True:
            total_illegals += 1
        total_rewards += resulty
        i += 1
    print(f"{str(num_games)} played against a random opponent!")
    print(f"{str(total_illegals)} games where engine made illegal move.")
    print(f"{str(total_moves / num_games)} moves made on average per game, legally.")
    print(f"{str(total_rewards / num_games)} average reward.")

def play_game_with_human(model = False):
    # Initialize the chess board and engine
    board = chess.Board()
    #engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    did_illegal = False
    # Choose the player's color randomly
    player_color = chess.WHITE if bool(random.getrandbits(1)) else chess.BLACK

    # Initialize the moves list
    moves_list = []
    comp_colour = 0 if player_color == chess.WHITE else 1
    #print(comp_colour)
    #comp_colour = 0
    #print(player_color)
    comp_colour = 1
    flag = 0
    flaggy = False
    player_color = chess.BLACK
    # Play the game
    while not board.is_game_over():
        if board.turn == player_color or flaggy == True:
            print_pos(board)
            if flag == 0:
                print("It's chessGPT's turn!")
                print("Please wait for the computer to move:")
                print(" ")
                print(" ")
                print(" ")
            real_valid_move = False
            invalid_count = 0
            while real_valid_move == False:
                valid_move = False
                # Get the player's move
                #print(movess)
                #for move in moves_list:
                    #print(type(move))
                if model == False:
                    while valid_move == False:
                        try:
                            player_move = chessGPT(board, moves_list, comp_colour) # Replace with your own implementation
                            if player_move == False:
                                invalid_count += 1
                                if invalid_count > 3:
                                    return len(moves_list), True, 0
                            valid_move = True
                        except:
                            invalid_count += 1
                            if invalid_count > 3:
                                return len(moves_list), True, 0
                    
                else:
                    while valid_move == False:
                        try:
                            player_move = chessGPT(board, moves_list, comp_colour, model) # Replace with your own implementation
                            if player_move == False:
                                invalid_count += 1
                                if invalid_count > 3:
                                    return len(moves_list), True, 0
                            valid_move = True
                        except:
                            invalid_count += 1
                            if invalid_count > 3:
                                return len(moves_list), True, 0
                # Make the move on the board
                moveyy = chess.Move.from_uci(player_move)
                #print(player_move)
                try:
                    if moveyy in list(board.legal_moves):
                        board.push(moveyy)
                        moves_list.append(moveyy)
                        real_valid_move = True
                    else:
                        invalid_count += 1
                        if invalid_count > 3:
                            return len(moves_list), True, 0
                except:
                    invalid_count += 1
                    if invalid_count > 3:
                        return len(moves_list), True, 0
                #print(board)
                #print(moves_list)
            # Add the move to the moves list
        else:
            print_pos(board)
            print("It's your turn! Type your move below:")
            print(" ")
            print(" ")
            print(" ")
            # Get the engine's move
            #time.sleep(1)
            valid_move = False
            has_tried = False
            while valid_move == False:
                if has_tried == True:
                    
                    print("Invalid move. Please try again.")
                try:
                    #result = engine.play(board, chess.engine.Limit(time=1))
                    human_move = str(input("enter move:"))
                    if human_move == "end":
                        print("Game restarted.")
                        return
                    #engine_move = result.move
                    # Make the move on the board
                    board.push_san(human_move)
                    valid_move = True
                except:
                    has_tried = True
            #print(board)
            moves_list.append(board.move_stack[-1])
            #print(moves_list)
            # Add the move to the moves list

    # Close the engine
    #engine.quit()
    import time
    if board.result() == "1-0":
        result = 0
        print("YOU WON!")
        time.sleep(5)
    elif board.result() == "0-1":
        result = 1
        print("YOU LOST!")
        time.sleep(5)
    else:
        result = 0.5
        print("DRAW!")
        time.sleep(5)
        
    # Return the final board and moves list
    return len(moves_list), did_illegal, result

while True:
    play_game_with_human()
