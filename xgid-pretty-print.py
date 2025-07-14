
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
    'k': 11, 'K': 11, 'l': 12, 'L': 12, 'm': 13, 'M': 13, 'n': 14, 'N': 14, 'o': 15, 'O': 15,
    'p': 16, 'P': 16, 'q': 17, 'Q': 17, 'r': 18, 'R': 18, 's': 19, 'S': 19, 't': 20, 'T': 20
}

CUBE_POSITION = {'0': 'CENTERED', '1': 'BOTTOM/P1', '2': 'TOP/P2'}
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
    print("Cr:"+str(crawford), "L:"+str(length), "T:"+str(player_top_score), "B:"+str(player_bottom_score))
    if str(crawford) == "1":
        return "CRAWFORD"
    length = int(length)
    top = int(player_top_score)
    bottom = int(player_bottom_score)
    if length == 0 or length == 1 : return "-"
    if str(crawford) == "0" and (top == length - 1 or bottom == length - 1):
        return "POST-CRAWFORD"
    return "-"

def xgid_details_string(xgid, indented=False, raw=False):
    """
    Receives an XGID string and returns a formatted string with all field details.
    If indented=True, uses the indented template.
    """
    if xgid.startswith("XGID="):
        xgid = xgid[5:]
    raw_parts = xgid.split(":")
    # Add bottom and top bar from the board part
    raw_parts.append(raw_parts[0][0])
    raw_parts.append(raw_parts[0][25])
    while len(raw_parts) < 12:
        raw_parts.append('-')
    
    output_parts = raw_parts
    if not raw:
        output_parts[10] = PIECE_MAP[output_parts[10]]
        output_parts[11] = PIECE_MAP[output_parts[11]]
        output_parts[1] = "x"+str(2**(int(output_parts[1])))
        output_parts[2] = CUBE_POSITION[output_parts[2]]
        output_parts[3] = TURN_PLAYER[output_parts[3]]
        output_parts[7] = crawford_status_string(output_parts[7], output_parts[8], output_parts[5], output_parts[6])

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
    if xgid.startswith("XGID="):
        xgid = xgid[5:]
    # The first char is bottom bar, next 24 are points 1-24, last char is top bar
    xgid_parts = xgid.split(":")[0]
    if len(xgid_parts) != 26:
        raise ValueError("XGID board part must be 26 characters (bar + 24 points + bar)")
    bottom_bar = xgid_parts[0]
    points = xgid_parts[1:25]
    top_bar = xgid_parts[25]

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
    max_height = max(max(len(p) for p in top_points), max(len(p) for p in bottom_points), 5)

    header = "  13 14 15 16 17 18      19 20 21 22 23 24"
    footer = "  12 11 10  9  8  7       6  5  4  3  2  1"
    sep = "+-------------------+---+------------------+"
    bar_label = "|                   |BAR|                  |"

    lines = [header, sep]
    # Top row (align to top)
    for row in range(max_height):
        line = "| "
        for i in range(6):
            pt = top_points[i]
            line += " {:<2}".format(pt[row] if row < len(pt) else "")
        line += "|   |"
        for i in range(6, 12):
            pt = top_points[i]
            line += " {:<2}".format(pt[row] if row < len(pt) else "")
        line += "|"
        lines.append(line)
    lines.append(bar_label)
    # Bottom row (align to bottom)
    for row in range(max_height):
        line = "| "
        for i in range(6):
            pt = bottom_points[i]
            idx = row - (max_height - len(pt))
            line += " {:<2}".format(pt[idx] if 0 <= idx < len(pt) else "")
        line += "|   |"
        for i in range(6, 12):
            pt = bottom_points[i]
            idx = row - (max_height - len(pt))
            line += " {:<2}".format(pt[idx] if 0 <= idx < len(pt) else "")
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


def xgid_str(xgid, board=True, details=True, input=True):
    output = []
    if input: output.append(xgid+'\n')
    if board: output.append(xgid_board_string(xgid)+'\n')
    if details: output.append(xgid_details_string(xgid, True, False)+'\n')
    return ''.join(output)

def main():
    print("=============== START ===============")
    #xgid = "XGID=-b----E-C---eE---c-e----B-:0:0:1:65:0:0:0:1:10"
    xgid = "XGID=fb---AG-CA--eD---c-g----Bg:2:0:-1:55:3:10:0:11:10"
    print(xgid_details_string(xgid, indented=True, raw=True))
    print("======================================")
    print(xgid_details_string(xgid, indented=True, raw=False))
    print("======================================")
    print(xgid_board_string(xgid))
    print("=============================================")
    print(crawford_status_string(1, 11, 10, 5))  # "CRAWFORD"
    print(crawford_status_string(0, 11, 10, 5))  # "POST-CRAWFORD"
    print(crawford_status_string(0, 11, 9, 5))   # ""

    print(xgid_str(xgid))

if __name__ == "__main__":
    main()
    