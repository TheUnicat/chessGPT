import chess
import random
def clean_file(input_file, output_file, save_interval):
    done = 0
    with open(input_file, 'rb') as f_in:
        with open(output_file, 'w') as f_out:
            line_count = 0
            for line in f_in:
                try:
                    line = line.decode("utf-8")
                except:
                    continue
                if not line.startswith('['):
                    f_out.write(line)
                    line_count += 1
                if line_count % save_interval == 0:
                    done += 1
                    print(done, " million lines done!")
                    f_out.flush()
                

input_file = 'DATABASE4U.txt'
output_file = 'clean_chess.txt'
save_interval = 1000000

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

def sanitize_file(input_file, output_file):
    with open(input_file, 'r') as f_in:
        with open(output_file, 'w') as f_out:
            new_line = ""
            end_sequence = ""
            line_count = 0
            end = False
            ends = ["*", "1-0", "0-1", "1/2-1/2"]
            for line in f_in:
                for char in line:
                    if end == True:
                        final_new_line = "[[[[[" + end_sequence + "]]]]]" + " " + new_line.strip() + "\n\n"
                        if "(" not in final_new_line:
                            if ")" not in final_new_line: 
                                f_out.write(final_new_line)
                        line_count += 1
                        if line_count % 10000 == 0:
                            print(f"{line_count // 10000} ten thousand games done!")
                        end = False
                        new_line = ""
                        end_sequence = ""
                    end_sequence += char
                    dont_stop = False
                    for thing in ends:
                        if end_sequence == thing:
                            end = True
                            dont_stop = True
                            break
                        elif end_sequence in thing:
                            dont_stop = True
                            break
                    if not dont_stop:
                        new_line += end_sequence
                        end_sequence = ""
                        
                    if end_sequence == "":
                        #new_line += char
                        pass
    print(f"Total of {line_count} games done!")

input_file = 'clean_chess.txt'
output_file = 'sanitized_chess.txt'

def even_more_sanitize(input_file, output_file):
    with open(input_file, 'r') as f_in:
        with open(output_file, 'w') as f_out:
            in_bracket = False
            in_paren = False
            line_count = 0
            paren_count = 0
            for line in f_in:
                new_line = ""
                i = 0
                while i < len(line):
                    char = line[i]
                    if char == '(':
                        in_paren = True
                        paren_count += 1
                    elif char == ')':
                        paren_count += -1
                        if paren_count == 0:
                            in_paren = False
                        i += 2
                        if in_paren == False:
                            j = i
                            while j < len(line) and line[j].isdigit():
                                j += 1
                                i += 1
                            if j < len(line) and line[j:j+3] == "...":
                                i = j + 3
                                while i < len(line) and line[i].isspace():
                                    i += 1
                    elif in_paren:
                        i += 1
                    elif char == '$':
                        i += 1
                        j = i
                        while i < len(line) and line[i].isdigit():
                            i += 1
                        while i < len(line) and line[i].isspace():
                            i += 1
                    else:
                        new_line += char
                        i += 1
                f_out.write(new_line)
                line_count += 1
                print("hi")
                if line_count % 100 == 0:
                    print(f"{line_count // 1000000} ten thousand lines done!")

output_file = 'finished_chess.txt'
input_file = 'even_more_sanitized_chess.txt'

def sanitizere_file():
    with open("sanitized_chess.txt", "r") as file:
        lines = file.readlines()
        
    with open("even_more_sanitized_chess.txt", "w") as file:
        counter = 0
        flag = False
        nested = 0
        dollar_counter = 0
        flag_count = 0
        for line in lines:
            new_line = ""
            
            for char in line:
                if flag_count > 3:
                    flag_count = 0
                    flag = False
                    new_line += char
                elif char == '$':
                    flag = True
                    dollar_counter += 1
                    flag_count = 1
                elif char.isdigit() and flag:
                    flag_count += 1
                
                elif not char.isdigit() and flag:
                    flag = False
                    flag_count = 0
                    new_line += char
                elif flag == False:
                    new_line += char
                elif flag:
                    flag_count += 1
                    
            file.write(new_line)
            counter += 1
            
            if counter % 1000000 == 0:
                print(f"{counter // 1000000} million lines processed")
                print(dollar_counter)
                

def pad_string(s):
    while len(s) < 4:
        s = '[' + s
    return s

def process_moves(filename, outfile):

    with open(filename, 'r') as f, open(outfile, 'w') as out:
        line_number = 0
        thing = True
        nummy = False
        for line in f:
            if thing == True:
                thing = False
                print(line)
            stripped_line = ''
            for char in line:
                if char.isdigit():
                    if nummy == False:
                         nummy = char
                         continue
                    nummy += char
                    continue
                if nummy != False:
                    if char == ".":
                        nummy = False
                        continue
                    stripped_line += nummy
                    nummy = False
                stripped_line += char
            if nummy != False:
                stripped_line += nummy
            nummy = False
            out.write(stripped_line)
            line_number += 1
            if line_number % 100000 == 0:
                print(f'Processed {line_number / 100000} hundred thousand lines')


filenamey = "results_in_front.txt"
outfiley = "processed_chess.txt"
print("hi!")
#sanitize_file("even_more_sanitized_chess.txt", "results_in_front.txt")
print("DONE!!!!!!")
# open processed_chess.txt in read mode and individual_chess.txt in write mode
def cleaner():
    game = 0
    bypass = True
    with open("processed_chess.txt", "r") as processed_file, open("individual_chess.txt", "w") as individual_file:
        new_line = "" # initialize an empty string to store each game
        for line in processed_file:
            # if the line starts with "[[[[[", this means it is a result line and a new game is starting
            #print(line[:5])
            if line.startswith("[[[[["):
                if bypass == True:
                    new_line += line
                    bypass = False
                    continue
                # if new_line is not empty, this means we have a previous game that needs to be written to individual_chess.txt
                else:
                    new_line = new_line.replace("\n", " ")
                    individual_file.write(new_line)
                    individual_file.write("\n")
                    individual_file.write("\n")
                    new_line = "" # reset new_line to be an empty string
                    new_line += line # add the result line to new_line
                    game += 1
                    if game %  10000 == 0:
                        print(f'{game/10000} ten thousand games done!')
            else:
                new_line += line
                # if it is not a result line, remove the newline characters and add the line to new_line
        new_line = new_line.replace("\n", " ")
        # write the last game to individual_chess.txt
        individual_file.write(new_line)

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

def add_boards():
    with open("processed_chess.txt", "r") as f, open("10000_base.txt", "w") as to_write:
        counter = 0
        import time
        time_start = time.time()
        for line in f:
            if line != "" and line != " " and line != "\n":
                counter += 1
                if counter == 10000:
                    time_end = time.time()
                    print(time_end - time_start)
                    aew
                board = chess.Board()
                new_line = ""
                source = line.split(" ")
                #print(source)
                moves = source[1:-1]
                for element in moves:
                    if element == "":
                        moves.pop(moves.index(element))
                #print(moves)
                result = source[0].strip("[").strip("]")
                #print(result)
                # convert result to a scalar value
                if result == "1-0":
                    reward = -1 * len(moves) + 1
                elif result == "0-1":
                    reward = len(moves) - 1
                else:
                    reward = ","
                #print(reward)
                if reward == ",":
                    for move in moves:
                        new_line += ","
                        new_line += move
                        try:
                            board.push_san(move)
                            new_line += board_encoding(board)
                        except:
                            new_line = ""
                            break
                elif reward < 0:
                    for move in moves:
                        new_line += str(reward)
                        reward += 1
                        new_line += move
                        try:
                            board.push_san(move)
                            new_line += board_encoding(board)
                        except:
                            new_line = ""
                            break
                else:
                    for move in moves:
                        new_line += str(reward)
                        reward += -1
                        new_line += move
                        try:
                            board.push_san(move)
                            new_line += board_encoding(board)
                        except:
                            new_line = ""
                            break
                to_write.write(new_line)
                #print(new_line)
                
def game_encoder(reward, inputy):
    board = chess.Board()
    inputy = inputy.replace("  ", " ")
    moves = inputy.split(" ")
    print(moves)
    out_list = []
    if reward == ",":
        for move in moves:
            new_line = ""
            new_line += ","
            new_line += move
            board.push_san(move)
            new_line += board_encoding(board)
            out_list.append(new_line)
    elif reward < 0:
        for move in moves:
            new_line = ""
            new_line += str(reward)
            reward += 1
            new_line += move
            board.push_san(move)
            new_line += board_encoding(board)
            out_list.append(new_line)
    else:
        for move in moves:
            new_line = ""
            new_line += str(reward)
            reward += -1
            new_line += move
            board.push_san(move)
            new_line += board_encoding(board)
            out_list.append(new_line)
    if len(out_list) < 3:
        returny = ""
        for thing in out_list:
            returny += thing
        return returny
    else:
        return out_list[-3] + out_list[-2] + out_list[-1]
#print(game_encoder(3, "f3 e5 g4"))

def new_add_boards():
    with open("processed_chess.txt", "r") as f, open("2_million_base.txt", "w") as to_write:
        counter = 0
        import time
        print("hi!")
        time_start = time.time()
        for line in f:
            colour = random.randint(0, 1)
            if line != "" and line != " " and line != "\n":
                counter += 1
                if counter < 500000:
                    continue
                if counter == 2000000:
                    time_end = time.time()
                    print(time_end - time_start)
                    return
                elif counter % 5000 == 0:
                    print(f"{str(counter / (5000 * 4))}% done!")
                board = chess.Board()
                new_line = ""
                source = line.split(" ")
                #print(source)
                moves = source[1:-1]
                for element in moves:
                    if element == "":
                        moves.pop(moves.index(element))
                #print(moves)
                result = source[0].strip("[").strip("]")
                #print(result)
                # convert result to a scalar value
                if result == "1-0":
                    if colour == 0:
                        if len(moves) % 2 != 0:
                            reward = "H" + str((len(moves) - 1) / 2)
                        else:
                            moves.pop(-1)
                            reward = "H" + str((len(moves) - 1) / 2)
                    else:
                        if len(moves) % 2 != 0:
                            reward = "X" + str((len(moves) - 3) / 2)
                        else:
                            moves.pop(-1)
                            reward = "X" + str((len(moves) - 3) / 2)
                elif result == "0-1":
                    if colour == 0:
                        if len(moves) % 2 != 0:
                            moves.pop(-1)
                            reward = "X" + str((len(moves) - 2) / 2)
                        else:
                            reward = "X" + str((len(moves) - 2) / 2)
                    else:
                        if len(moves) % 2 != 0:
                            moves.pop(-1)
                            reward = "H" + str((len(moves) - 2) / 2)
                        else:
                            reward = "H" + str((len(moves) - 2) / 2)
                else:
                    reward = ","
                #print(reward)
                if reward == ",":
                    if colour == 0:
                        move_side = 0
                        for move in moves:
                            if move_side == 0:
                                move_side = 1
                                new_line += ",[[[["
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
                                new_line += ",[[[["
                                try:
                                    board.push_san(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "w"
                            else:
                                move_side = 1
                                try:
                                    board.push_san(move)
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
                                new_line += "H"
                                new_line += pad_string(str(reward))
                                reward += -1
                                try:
                                    board.push_san(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "w"
                            else:
                                move_side = 1
                                try:
                                    board.push_san(move)
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
                                    board.push_san(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "w"
                            else:
                                move_side = 1
                                try:
                                    board.push_san(move)
                                    new_line += board_encoding(board)
                                except:
                                    new_line = ""
                                    break
                to_write.write(new_line)
                #print(new_line)

#new_add_boards()

def decode_to_move(input_string, output_string):
    files = {1: 'a', 2: 'b', 3: 'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h'}
    output_string = output_string[len(input_string):]
    for char in output_string:
        if char == "w" or char == "W":
            move = output_string[(output_string.index(char) - 5):(output_string.index(char))]
            from_square = move[:2]
            to_square = move[2:4]
            promotion = move[-1]
            for value in move[:-1]:
                try:
                    if int(value) not in range(1, 9):
                        print(f"Error. Value {str(value)} not a valid file or rank. Files or ranks must be numbers between 1-8.")
                        return
                except:
                    print(f"Error. Value {str(value)} not a valid file or rank. Files or ranks must be numbers between 1-8.")
                    return
            decoded_move = ""
            decoded_move += str(files[int(from_square[0])])
            decoded_move += str(int(from_square[1]) + 1)
            decoded_move += str(files[int(to_square[0])])
            decoded_move += str(int(to_square[1]) + 1)
            print(decoded_move)
            return
    print("Error: Illegal move. No player specified.")
    return
                
def new_game_encoder(colour, reward, inputy):
    if 1 == 1:
        if 2 == 2:
            if 3 == 3:
                board = chess.Board()
                new_line = ""
                moves = inputy.split(" ")
                for move in moves:
                    if move == " " or move == "\n":
                        moves.pop(moves.index(move))
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
                                new_line += pad_string(",")
                                try:
                                    board.push_san(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "w"
                            else:
                                move_side = 1
                                try:
                                    board.push_san(move)
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
                                    board.push_san(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "w"
                            else:
                                move_side = 1
                                try:
                                    board.push_san(move)
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
                                    board.push_san(move)
                                except:
                                    new_line = ""
                                    break
                                new_line += algebraic_to_coord(move, board)
                                new_line += "w"
                            else:
                                move_side = 1
                                try:
                                    board.push_san(move)
                                    new_line += board_encoding(board)
                                except:
                                    new_line = ""
                                    break
    if len(new_line) >= 400:
        new_line = new_line[len(new_line) - 400:]
    print(new_line)
    #print(moves)
    inputy = input("Enter response:")
    print(decode_to_move(new_line, inputy))
#new_game_encoder(20, "H40", """d4 Nf6 c4 e6 Nf3 b6 g3 Ba6 b3 Bb4+ Bd2 Be7 Bg2 O-O O-O d5 Nc3 c6 Bf4 Nbd7 cxd5 exd5 Ne1 Re8 Nd3 Nf8 Bg5 Ne6 Bxf6 Bxf6 e3""")


#decode_to_move("""rnbqkbnrpppppppp-------------------P------------PPP-PPPPRNBQKBNRYYYYH404644Mwrn
#bqkbnrppp-pppp-----------p------PP------------PP--PPPPRNBQKBNRYYYYH394433Mwrnbqkbnrppp-pppp------------------pP--------P---PP---PPPRNBQKBNRYYYY""", """rnbqkbnrppp
#ppppp-------------------P------------PPP-PPPPRNBQKBNRYYYYH404644Mwrnbqkbnrppp-pppp-----------p------PP------------
    #           PP--PPPPRNBQKBNRYYYYH394433Mwrnbqkbnrppp-pppp------------------pP--------P---PP---PPPRNBQKBNRYYYYH[[387765Mwrnbqkb-rppp-pppp-----n------------pP--------P-N-PP---PPPRNBQKB-RY""")


