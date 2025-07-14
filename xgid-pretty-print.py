import sys
#      Bottom player BAR position
#      |                        Top player BAR position
#      |                        | Cube Value: 0=*(2^0), 1=*(2^1), 2=*(2^2), 3=*(2^3), ...
#      |                        | | Cube position: 0=center, 1=bottom, -1=top 
#      |                        | | | turn: 1 = (bottom) player 1's turn, -1 = (top) player 2's turn
#      |                        | | | | Current dice values: dice1, dice2. 00 if not rolled. D on cube decision
#      |                        | | | | |  player1_score (bottom)
#      |                        | | | | |  | player2_score (top)
#      |                        | | | | |  | | crawford-state: 0=pre-crawford or post-crawford, 1=crawford, 
#      |                        | | | | |  | | | match_length (0 for money game)
#      |                        | | | | |  | | | | default value 10
#      |                        | | | | |  | | | | |
# XGID=-b----E-C---eE---c-e----B-:0:0:1:65:0:0:0:1:10

# Map XGID chars to number of pieces
PIECE_BOTTOM = 'B'
PIECE_TOP = 'T'

PIECE_MAP = {
    '-': 0, 'a': 1, 'A': 1, 'b': 2, 'B': 2, 'c': 3, 'C': 3, 'd': 4, 'D': 4, 'e': 5, 'E': 5,
    'f': 6, 'F': 6, 'g': 7, 'G': 7, 'h': 8, 'H': 8, 'i': 9, 'I': 9, 'j': 10, 'J': 10,
    'k': 11, 'K': 11, 'l': 12, 'L': 12, 'm': 13, 'M': 13, 'n': 14, 'N': 14, 'o': 15, 'O': 15
}

CUBE_POSITION = {'0': 'CENTERED', '1': 'BOTTOM/P1', '-1': 'TOP/P2'}
TURN_PLAYER = {'1': 'BOTTOM/P1', '-1': 'TOP/P2'}

def piece_char(c):
    if c == '-' or c.isdigit():
        return None
    return PIECE_TOP if c.islower() else PIECE_BOTTOM
    
def crawford_status_string(crawford, length, player_top_score, player_bottom_score):
    """
    Returns a string indicating the Crawford status.
    - Returns "CRAWFORD" if crawford == 1.
    - Returns "POST-CRAWFORD" if crawford == 0 and (player_top_score == length-1 or player_bottom_score == length-1).
    - Else, returns "".
    """
    #print("Cr:"+str(crawford), "L:"+str(length), "T:"+str(player_top_score), "B:"+str(player_bottom_score))
    if str(crawford) == "1":
        return "CRAWFORD"
    length = int(length)
    top = int(player_top_score)
    bottom = int(player_bottom_score)
    if length == 0 or length == 1 : return "-"
    if str(crawford) == "0" and (top == length - 1 or bottom == length - 1):
        return "POST-CRAWFORD"
    return "-"

def tokenize_xgid(xgid):
    """
    Takes an XGID string and returns a list of tokens, with bottom and top bar appended and padded to length 12.
    """
    if xgid.startswith("XGID="):
        xgid = xgid[5:]
    xgid_tokens = xgid.split(":")

    # gets the BAR pieces 
    xgid_tokens.append(xgid_tokens[0][0])
    xgid_tokens.append(xgid_tokens[0][25])
    while len(xgid_tokens) < 12:
        xgid_tokens.append('-')
    return xgid_tokens

def scoreboard_string(top_player_score, turn, length, crawford_state, bottom_player_score):
    lines = [
        f"          ",
        f"          ",
        f"     T:{int(top_player_score):2} ",   # 1st line
        f"          ",                                  # 2nd line
        f"   BOTTOM " if turn == '1' else "      TOP ", # 3rd line
        f"     TURN ",                         # 4th line
        f"          ",                                  # 5th line
        f"Length {length:2} ",                  # 6th line
        f"          ",                                  # 7th line
        f"     POST " if crawford_state == "POST-CRAWFORD" else "          ", # 8th line
        f" CRAWFORD " if crawford_state in ("CRAWFORD", "POST-CRAWFORD") else "          ", # 9th line
        f"          ",                                  # 10th line
        f"     B:{int(bottom_player_score):2} ", # 11th line
        f"          ",
        f"          "
    ]
    return "\n".join(lines)

def cube_string(cube_value, cube_position):
    cube = f"[{cube_value}]"
    lines = [
        f"",
        f"",
        cube if cube_position == '-1' else f"",
        f"",
        f"",
        f"",
        f"",
        f"[64]" if cube_position == '0' else f"",
        f"",
        f"",
        f"",
        f"",
        cube if cube_position == '1' else f"",
        f"",
        f""
    ]
    return "\n".join(lines)

def xgid_left_details_string(xgid):
    xgid_tokens = tokenize_xgid(xgid)
    turn = TURN_PLAYER[xgid_tokens[3]]
    top_player_score = xgid_tokens[5]
    bottom_player_score = xgid_tokens[6]
    crawford = xgid_tokens[7]
    length = xgid_tokens[8]
    crawford_state = crawford_status_string(crawford, length, top_player_score, bottom_player_score)
    return scoreboard_string(top_player_score, turn, length, crawford_state, bottom_player_score)

def xgid_right_details_string(xgid):
    xgid_tokens = tokenize_xgid(xgid)
    cube_value = cube_value = str(2**(int(xgid_tokens[1])))
    cube_position = xgid_tokens[2]
    return cube_string(cube_value, cube_position)

def xgid_details_string(xgid, indented=False, raw=False):
    """
    Receives an XGID string and returns a formatted string with all field details.
    If indented=True, uses the indented template.
    """
    xgid_tokens = tokenize_xgid(xgid)
    
    bottom_player_bar = PIECE_MAP[xgid_tokens[10]]
    top_player_bar = PIECE_MAP[xgid_tokens[11]]
    cube_value = "x"+str(2**(int(xgid_tokens[1])))
    cube_pos = CUBE_POSITION[xgid_tokens[2]]
    turn = TURN_PLAYER[xgid_tokens[3]]
    
    crawford_status = crawford_status_string(xgid_tokens[7], xgid_tokens[8], xgid_tokens[5], xgid_tokens[6])
    
    output_parts = xgid_tokens
    if not raw:
        output_parts[10] = bottom_player_bar
        output_parts[11] = top_player_bar
        output_parts[1] = cube_value
        output_parts[2] = cube_pos
        output_parts[3] = turn 
        output_parts[7] = crawford_status

    if indented:
        template = (
            "      Bottom player BAR : {10}\n"
            "         Top player BAR : {11}\n"
            "             Cube Value : {1}\n"
            "          Cube position : {2}\n"
            "                   Turn : {3}\n"
            "     Dice/Cube Decision : {4}\n"
            "(Bottom) Player 1 Score : {5}\n"
            "   (Top) Player 2 Score : {6}\n"
            "         Crawford-state : {7}\n"
            "           Match Length : {8}\n"
            "          Default Value : {9}"
        )
    else:
        template = (
            "Bottom player BAR ..... : {10}\n"
            "Top player BAR ........ : {11}\n"
            "Cube Value ............ : {1}\n"
            "Cube position ......... : {2}\n"
            "Turn .................. : {3}\n"
            "Dice/Cube Decision .... : {4}\n"
            "(Bottom) Player 1 Score : {5}\n"
            "(Top) Player 2 Score .. : {6}\n"
            "Crawford-state ........ : {7}\n"
            "Match Length .......... : {8}\n"
            "Default Value ......... : {9}"
        )
    return template.format(*output_parts)

def xgid_board_string(xgid):
    """
    Receives an XGID string and returns a string of the board checkers in a text-based format.
    Upper row: pieces aligned to the top.
    Lower row: pieces aligned to the bottom.
    Bottom player = 'B', Top player = 'T'.
    """
    xgid_tokens = tokenize_xgid(xgid)[0]
    if len(xgid_tokens) != 26:
        raise ValueError("XGID board part must be 26 characters (bar + 24 points + bar)")
    bottom_bar = xgid_tokens[0]
    points = xgid_tokens[1:25]
    top_bar = xgid_tokens[25]

    # Build points
    points_list = []
    for c in points:
        n = PIECE_MAP.get(c, 0)
        char = piece_char(c)
        points_list.append([char]*n if char else [])

    # Top row: points 13-24 (index 12-23)
    top_points = points_list[12:24]
    # Bottom row: points 12-1 (index 11-0, reversed)
    bottom_points = points_list[11::-1]
    # Set fixed height for piece rows
    piece_rows = 5

    header = "  13 14 15 16 17 18      19 20 21 22 23 24"
    footer = "  12 11 10  9  8  7       6  5  4  3  2  1"
    sep = "+-------------------+---+------------------+"
    bar_label = "|                   |BAR|                  |"

    lines = [header, sep]
    # Top row (align to top, always 5 rows)
    for row in range(piece_rows):
        line = "| "
        for i in range(6):
            pt = top_points[i]
            n = len(pt)
            if n > 5:
                if row < 4:
                    line += " {:<2}".format(pt[row] if row < n else "")
                elif row == 4:
                    line += " {:<2}".format(str(n))
                else:
                    line += "    "
            else:
                line += " {:<2}".format(pt[row] if row < n else "")
        line += "|   |"
        for i in range(6, 12):
            pt = top_points[i]
            n = len(pt)
            if n > 5:
                if row < 4:
                    line += " {:<2}".format(pt[row] if row < n else "")
                elif row == 4:
                    line += " {:<2}".format(str(n))
                else:
                    line += "    "
            else:
                line += " {:<2}".format(pt[row] if row < n else "")
        line += "|"
        lines.append(line)
    lines.append(bar_label)
    # Bottom row (align to bottom, always 5 rows)
    for row in range(piece_rows):
        line = "| "
        for i in range(6):
            pt = bottom_points[i]
            n = len(pt)
            if n > 5:
                if row == 0:
                    line += " {:<2}".format(str(n))
                else:
                    piece_idx = n - 5 + row
                    line += " {:<2}".format(pt[piece_idx] if 0 <= piece_idx < n else "")
            else:
                idx = row - (piece_rows - n)
                line += " {:<2}".format(pt[idx] if 0 <= idx < n else "")
        line += "|   |"
        for i in range(6, 12):
            pt = bottom_points[i]
            n = len(pt)
            if n > 5:
                if row == 0:
                    line += " {:<2}".format(str(n))
                else:
                    piece_idx = n - 5 + row
                    line += " {:<2}".format(pt[piece_idx] if 0 <= piece_idx < n else "")
            else:
                idx = row - (piece_rows - n)
                line += " {:<2}".format(pt[idx] if 0 <= idx < n else "")
        line += "|"
        lines.append(line)
    lines.append(sep)
    lines.append(footer)
    return "\n".join(lines)

def xgid_full_game_board_string(xgid):
    board_str = xgid_board_string(xgid)

# Crear una funcion que cuenta las fichas de cada jugador
# deberían tener 15 cada uno
# caso contrario, se asume que son fichas fuera de juego 
# ejemplo: si el jugador tiene 10 fichas en juego,
#   entonces tiene 5 fichas fuera de juego

    fgb_str = ""

    return fgb_str

def print_columns(arr1, arr2, arr3):
    max_len = max(len(arr1), len(arr2), len(arr3))
    # Pad arrays to max_len
    arr1 = arr1 + ["" for _ in range(max_len - len(arr1))]
    arr2 = arr2 + ["" for _ in range(max_len - len(arr2))]
    arr3 = arr3 + ["" for _ in range(max_len - len(arr3))]
    for i in range(max_len):
        print(f"{arr1[i]}{arr2[i]}{arr3[i]}")

def xgid_str(xgid, board=True, details=True, input=True):
    output = []
    if input: output.append(xgid+'\n')
    if board: output.append(xgid_board_string(xgid)+'\n')
    if details: output.append(xgid_details_string(xgid, True, False)+'\n')
    return ''.join(output)

def xgid_pretty_print(xgid, board=True, details=True, input=True):
    if input: print(xgid+'\n')
    center_board = xgid_board_string(xgid)
    left_side = xgid_left_details_string(xgid)
    right_side = xgid_right_details_string(xgid)
    print_columns(left_side.splitlines(), center_board.splitlines(), right_side.splitlines())
    print()
    if details: print(xgid_details_string(xgid, True, False))


def main():
    print("=============== START ===============")
    if len(sys.argv) > 1:
        xgid = sys.argv[1]
    else:
        print("no XGID input found, try this one:")
        print("XGID=-b----E-C---eE---c-e----B-:0:0:1:65:0:0:0:1:10")
        return
    xgid_pretty_print(xgid)

if __name__ == "__main__":
    main()
    
