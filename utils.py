# static functions 
from typing import List
import pandas as pd


def get_person_boards(name: str) -> List[str]:
    """
    Retrieve unique boards associated with a person from CSV data.
    
    Args:
        name: Person's name to search (case insensitive)
        csv_path: Path to membership CSV file
        
    Returns:
        List of unique board names (empty list if no matches)
    """

    # Read CSV data
    df = pd.read_csv("generated_files/members.csv")
    
    # Filter and extract boards (case-insensitive match)
    return df.loc[
        df['name'].str.lower() == name.strip().lower(),
        'L1_Board'
    ].unique().tolist()

def board_under_L2_board(board: str) -> List[str]:
    """
    Retrieve all L2 boards associated with a given board from CSV data.
    
    Args:
        board: Board name to search (case insensitive)
        csv_path: Path to membership CSV file
        
    Returns:
        List of unique L2 board names (empty list if no matches)
    """

    if(board=="APS"):
        return ["APS1","APS2"]
    elif(board=="TES"):
        return ["TES1","TES2"]
    else:
        return ["CDF","EBSNF"]
