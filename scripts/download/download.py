from typing import Any, Dict, List, Optional
from typing import Boolean

def download(filename: str, filepath: str, variables: Dict[str, Any]) -> Boolean:
    """
    Download your custom dataset from the source to the download path. Return True if successful, False otherwise.
    """
    pass

if __name__ == "__main__":
    args = parse_args()
    if download(args.filename, args.filepath, args.variables):
        print(f"Downloaded dataset {args.filename} to {args.filepath} successfully.")
        exit(0)
    else:
        print(f"Downloaded dataset {args.filename} to {args.filepath} failed. 🤔")
        exit(1)
    try:
        validate_after_download(args.filename, args.filepath)
    except Exception as e:
        print(f"Validation failed: {e}. Look like the file went to somewhere else instead. Where is it? 🤔")
        exit(1)
    else:
        print(f"Validation passed.")
        exit(0)
    
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, required=True)
    parser.add_argument("--filepath", type=str, required=True)
    parser.add_argument("--variables", type=Dict[str, Any], required=True)
    return parser.parse_args()

def validate_after_download(filename: str, filepath: str) -> None:
    # Check if the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} does not exist.")
    # Check if the file is not empty
    if os.path.getsize(filepath) == 0:
        raise ValueError(f"File {filepath} is empty.")
    # Check if the file has the correct name
    if filename != os.path.basename(filepath):
        raise ValueError(f"File {filepath} has the incorrect name. Expected {filename}, got {os.path.basename(filepath)}.")
    return True