import argparse
import logging
import os
from typing import Any, Dict

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

def download(filename: str, filepath: str, variables: Dict[str, Any]) -> bool:
    """
    Download your custom dataset from the source to the download path. Return True if successful, False otherwise.
    """
    log.info(f"🚀 Initiating download mission for '{filename}'... Houston, we have a dataset.")
    log.debug(f"📋 Variables received: {variables}. Hopefully they mean something to you.")
    # TODO: implement your download logic here
    log.warning("📭 download() is still a stub. Nothing was actually fetched. Implement me!")
    pass

def validate_after_download(filename: str, filepath: str) -> None:
    log.info(f"🔍 Interrogating the file at '{filepath}'... let's see if it actually showed up.")
    if not os.path.exists(filepath):
        log.error(f"👻 '{filepath}' is a ghost — it doesn't exist. Did it go on vacation?")
        raise FileNotFoundError(f"File {filepath} does not exist.")
    if os.path.getsize(filepath) == 0:
        log.error(f"📄 '{filepath}' has zero bytes. A file with nothing inside — very zen, but useless.")
        raise ValueError(f"File {filepath} is empty.")
    if filename != os.path.basename(filepath):
        log.error(f"🏷️ Name mismatch! Expected '{filename}', got '{os.path.basename(filepath)}'. Did it change its name mid-flight?")
        raise ValueError(f"File {filepath} has the incorrect name. Expected {filename}, got {os.path.basename(filepath)}.")
    log.info(f"✅ '{filename}' checks out — exists, has content, and knows its own name. Truly a well-adjusted file.")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a dataset from a remote source.")
    parser.add_argument("--filename", type=str, required=True)
    parser.add_argument("--filepath", type=str, required=True)
    parser.add_argument("--variables", type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    log.info(f"📦 Download script just woke up. Target: '{args.filename}' → '{args.filepath}'.")
    try:
        if not download(args.filename, args.filepath, args.variables):
            log.error(f"💀 Download of '{args.filename}' returned False. The dataset ghosted us.")
            exit(1)
        log.info(f"🛬 '{args.filename}' landed. Now checking if it actually survived the trip...")
        validate_after_download(args.filename, args.filepath)
        log.info(f"🎉 Post-download validation passed. The file is real — not a figment of our imagination.")
        exit(0)
    except Exception as e:
        log.error(f"🔥 Something blew up: {e}. Look like the file went somewhere else instead.")
        exit(1)
