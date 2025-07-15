import sys
import pyperclip

def swap_chairs_xgid(xgid):
    """
    Swaps the chairs in an XGID string:
    - Board pieces are reversed (positions 1-24 swapped)
    - Cube position: 1 ↔ -1
    - Player scores swapped
    - Turn: 1 ↔ -1
    """
    if xgid.startswith("XGID="):
        xgid = xgid[5:]
    
    parts = xgid.split(":")
    if len(parts) < 9:
        raise ValueError("Invalid XGID format")
    
    # Extract board part (first part)
    board = parts[0]
    if len(board) != 26:
        raise ValueError("Board part must be 26 characters")
    
    # Reverse the board pieces (positions 1-24, keep bars at positions 0 and 25)
    bottom_bar = board[0]
    top_bar = board[25]
    points = board[1:25]
    
    # Reverse the points
    reversed_points = points[::-1]
    
    # Swap case for each piece (lower-case ↔ upper-case)
    case_swapped_points = ""
    for char in reversed_points:
        if char.islower():
            case_swapped_points += char.upper()
        elif char.isupper():
            case_swapped_points += char.lower()
        else:
            case_swapped_points += char  # Keep non-letters unchanged
    
    # Rebuild board with reversed and case-swapped points
    new_board = bottom_bar + case_swapped_points + top_bar
    
    # Swap cube position (1 ↔ -1)
    cube_pos = parts[2]
    new_cube_pos = "-1" if cube_pos == "1" else "1"
    
    # Swap turn (1 ↔ -1)
    turn = parts[3]
    new_turn = "-1" if turn == "1" else "1"
    
    # Swap player scores
    player1_score = parts[5]
    player2_score = parts[6]
    
    # Build new XGID
    new_parts = [
        new_board,      # 0: board
        parts[1],       # 1: cube value (unchanged)
        new_cube_pos,   # 2: cube position (swapped)
        new_turn,       # 3: turn (swapped)
        parts[4],       # 4: dice (unchanged)
        player2_score,  # 5: player1_score (was player2)
        player1_score,  # 6: player2_score (was player1)
        parts[7],       # 7: crawford (unchanged)
        parts[8],       # 8: match length (unchanged)
    ]
    
    # Add remaining parts if they exist
    if len(parts) > 9:
        new_parts.extend(parts[9:])
    
    return "XGID=" + ":".join(new_parts)

def main():
    debug_mode = False
    clipboard_mode = False
    xgid = None
    
    # Parse command line arguments
    for arg in sys.argv[1:]:
        if arg == "-d":
            debug_mode = True
        elif arg == "-c":
            clipboard_mode = True
        elif not arg.startswith("-"):
            xgid = arg
    
    if xgid is None:
        print("Usage: python xgid-swap-chairs.py [-d] [-c] <XGID>")
        print("  -d: debug mode (show input and output labels)")
        print("  -c: copy output to clipboard")
        print("Example:")
        print("python xgid-swap-chairs.py XGID=-a---aE-D---dD---c-d-AbA--:1:-1:1:41:0:2:0:5:10")
        return
    
    swapped = swap_chairs_xgid(xgid)
    
    if debug_mode:
        print(f"Input:  {xgid}")
        print(f"Output: {swapped}")
    else:
        print(swapped)
    
    if clipboard_mode:
        pyperclip.copy(swapped)
        if debug_mode:
            print("(Output copied to clipboard)")

if __name__ == "__main__":
    main()
