import argparse
import logging
import os
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

def compile(input_path: str, output_path: str, variables: Dict[str, Any]) -> bool:
    """
    Compile the input dataset into the output format. Return True if successful, False otherwise.
    """
    log.info(f"🏭 Compilation factory is open. Raw data goes in at '{input_path}', trained beauty comes out at '{output_path}'.")
    log.debug(f"🔧 Variables on the workbench: {variables}.")
    # TODO: implement your compilation logic here
    log.warning("🚧 compile() is still a stub. No actual transformation happened. Implement me!")
    pass

def validate_after_compile(output_path: str, extensions: List[str]) -> None:
    log.info(f"🧪 Running quality control on '{output_path}'... the inspector is strict.")
    if not os.path.exists(output_path):
        log.error(f"🕳️ '{output_path}' doesn't exist. The compiler may have eaten it.")
        raise FileNotFoundError(f"File {output_path} does not exist.")
    if os.path.getsize(output_path) == 0:
        log.error(f"🫙 '{output_path}' is completely empty. We compiled... nothing? Bold move.")
        raise ValueError(f"File {output_path} is empty.")
    extension = os.path.splitext(output_path)[-1]
    if extension not in extensions:
        log.error(f"📎 Wrong extension! Got '{extension}', expected one of {extensions}. Close, but no cigar.")
        raise ValueError(f"File {output_path} has the incorrect extension. Expected {extensions}, got {extension}.")
    log.info(f"✅ Output file passes inspection — exists, non-empty, and has the right extension. Chef's kiss.")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile a raw dataset into a trainable format.")
    parser.add_argument("--input", type=str, required=True, dest="input_path")
    parser.add_argument("--output", type=str, required=True, dest="output_path")
    parser.add_argument("--extensions", type=str, nargs="+", required=True)
    parser.add_argument("--variables", type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    log.info(f"⚙️ Compile script reporting for duty. '{args.input_path}' → '{args.output_path}'.")
    try:
        if not compile(args.input_path, args.output_path, args.variables):
            log.error(f"💥 compile() returned False. Something went wrong with the compilation. Tragic.")
            exit(1)
        log.info(f"📐 Compilation done (allegedly). Running the post-compile sanity check...")
        validate_after_compile(args.output_path, args.extensions)
        log.info(f"🎊 Compilation and validation both passed. Raw data → trained dataset. Beautiful.")
        exit(0)
    except Exception as e:
        log.error(f"🔥 Validation exploded: {e}. Something went wrong with the compilation.")
        exit(1)
