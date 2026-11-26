"""
main.py — SnackStack Voice Assistant entry point.

Run from terminal:
    uv run snackstack               # text-only interactive loop
    uv run snackstack --voice       # voice input + voice output
    uv run snackstack --voice-out   # text input  + voice output
"""


import argparse
import uuid

from snackstack.graph import build_graph
from snackstack.logger import setup_logger

logger = setup_logger("snackstack.main")


class SnackStackAssistant:
    """Wires the compiled graph to CLI and voice I/O."""

    def __init__(self, voice: str = "nova", speak: bool = False):
        self.graph   = build_graph()
        self.thread_id = str(uuid.uuid4())

    @property
    def _config(self):
        return {"configurable": {"thread_id": self.thread_id}}



def run_text_loop(assistant: SnackStackAssistant):
    """REPL: type queries, get agent responses."""
    logger.info("SnackStack — Text mode")
    logger.info("Type a query and press Enter. Commands: reset | quit")

    while True:
        try:
            query = input("\nYou > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            break
        if query.lower() == "reset":
            assistant.reset()
            continue

        answer = assistant.ask(query)
        logger.info("SnackStack: %s", answer)

    logger.info("Goodbye — stay healthy!")


def main():
    parser = argparse.ArgumentParser(description="SnackStack Voice Assistant")
    parser.add_argument("--voice",     action="store_true", help="Full voice: mic + speaker")
    parser.add_argument("--voice-out", action="store_true", help="Text input + voice output")
    parser.add_argument("--tts-voice", default="nova",      help="TTS voice (default: nova)")
    args = parser.parse_args()

    speak = args.voice or args.voice_out
    assistant = SnackStackAssistant(voice=args.tts_voice, speak=speak)

    # if args.voice:
    #     run_voice_loop(assistant)
    # else:
    
    run_text_loop(assistant)
    

if __name__ == "__main__":
    main()