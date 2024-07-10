#!/usr/bin/env python3
import re
def remover(filename):
    pattern = r"^((\S+\s+\d+\s+IN\s+(?:NS|SOA)\s+)|(\S+\s+\d+\s+AWS\s+ALIAS\s+))"
    with open(filename, "r+") as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in lines:
            if not re.search(pattern, line):
                f.write(re.sub(r"\.\s+(\d+)\s+IN\s+", f".      1      IN      ", line))

if __name__ == "__main__":
  import sys
  if len(sys.argv) != 2:
    print("Usage: python3 remove_lines.py <filename>")
    exit(1)
  filename = sys.argv[1]
  remover(filename)
  print(f"Lines not matching the pattern removed from {filename} (if any).")
