#!/usr/bin/env python3
import sys
import os
import re
import subprocess
from typing import List, Tuple

FORBIDDEN_PATTERNS = {
    "F01_GREEK_SYMBOLS": (re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF]'), "Griechische Symbole verboten"),
    "F02_SPECIAL_OPERATORS": (re.compile(r'[\+\*\#\$\%\&\/\\\|]'), "Verbotene Sonderzeichen in ID"),
    "F04_GERMAN_UMLAUTS": (re.compile(r'[äöüÄÖÜß]'), "Umlaute verboten"),
    "F06_NON_ASCII": (re.compile(r'[^\x00-\x7F]'), "Nicht-ASCII-Zeichen erkannt")
}

B6_ID_PATTERN = re.compile(r'\b(b6_[a-zA-Z0-9_]+|B6_[a-zA-Z0-9_]+)\b')

def get_staged_files() -> List[str]:
    try:
        cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
        valid_exts = ('.py', '.c', '.h', '.go', '.sh', '.rs', '.md', '.json')
        return [f for f in files if f.endswith(valid_exts)]
    except Exception:
        return []

def check_file_calm_compliance(filepath: str) -> List[Tuple[int, str, str]]:
    violations = []
    if not os.path.exists(filepath):
        return violations

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_no, line in enumerate(f, 1):
                matches = B6_ID_PATTERN.findall(line)
                for ident in matches:
                    if ident.startswith("b6_"):
                        violations.append((line_no, ident, "R01/R02_FAIL: Kleingeschriebenes Präfix 'b6_'"))
                    elif not re.match(r'^B6_[A-Z0-9_]+$', ident):
                        violations.append((line_no, ident, "R02_FAIL: Ungültiges Format"))

                for code, (pattern, msg) in FORBIDDEN_PATTERNS.items():
                    if pattern.search(line):
                        if "B6_" in line or "b6_" in line or "CALM" in line:
                            violations.append((line_no, line.strip()[:60], f"{code}: {msg}"))
    except Exception as e:
        violations.append((0, filepath, f"Fehler beim Lesen: {e}"))

    return violations

def main():
    staged_files = get_staged_files()
    if not staged_files:
        print("CALM Pre-Commit Hook: Keine relevanten Dateien staged.")
        sys.exit(0)

    print(f"CALM Pre-Commit Hook: Prüfe {len(staged_files)} staged Datei(en)...")
    total_violations = 0

    for filepath in staged_files:
        violations = check_file_calm_compliance(filepath)
        if violations:
            print(f"\nCALM Violation in '{filepath}':")
            for line_no, item, reason in violations:
                print(f"   Line {line_no}: [{item}] -> {reason}")
                total_violations += 1

    if total_violations > 0:
        print(f"\nCOMMIT ABGEBROCHEN: {total_violations} CALM-Verstöße festgestellt!")
        sys.exit(1)

    print("CALM Validation Passed: Alle Bezeichner entsprechen Strang 2.")
    sys.exit(0)

if __name__ == "__main__":
    main()
