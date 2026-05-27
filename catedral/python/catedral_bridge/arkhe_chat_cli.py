#!/usr/bin/env python3
"""
ARKHE Chat CLI
Interacts with the local llama.cpp server running the ARKHE-OS GGUF model.
"""

import argparse
import json
import urllib.request
import urllib.error
import sys

def chat(prompt, url="http://localhost:8080/completion"):
    data = json.dumps({
        "prompt": prompt,
        "n_predict": 128,
        "temperature": 0.7,
        "stream": True
    }).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            print("ARKHE-OS: ", end="", flush=True)
            for line in response:
                line = line.decode('utf-8').strip()
                if line.startswith("data: "):
                    content = line[6:]
                    if content == "[DONE]":
                        break
                    try:
                        chunk = json.loads(content)
                        if "content" in chunk:
                            print(chunk["content"], end="", flush=True)
                    except json.JSONDecodeError:
                        pass
            print()
    except urllib.error.URLError as e:
        print(f"Error communicating with server: {e}")
        print("Make sure the llama.cpp server is running on http://localhost:8080")

def main():
    parser = argparse.ArgumentParser(description="ARKHE Chat CLI")
    parser.add_argument("--url", default="http://localhost:8080/completion", help="llama.cpp server URL")
    args = parser.parse_args()

    print("=== ARKHE OS Chat Interface ===")
    print("Type 'exit' or 'quit' to end the session.")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            if not user_input.strip():
                continue
            chat(user_input, url=args.url)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()