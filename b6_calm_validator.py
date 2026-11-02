#!/usr/bin/env python3
"""
B6 System - CALM Nomenklatur & DNA Code Validator (v1.0.0)
SYSTEM STATUS: rauschfrei.zertifiziert_by_b6fortress | TERMINATED_CLEAN
"""

import re
import sys
from typing import Dict, List, Any

class B6CALMValidator:
    # 6 Verbotene Zeichenklassen (Forbidden Chars)
    FORBIDDEN_PATTERNS = {
        "F01_GREEK_SYMBOLS": re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF]'), # Ω, Φ, etc.
        "F02_SPECIAL_OPERATORS": re.compile(r'[\+\*\#\$\%\&\/\\\|]'),
        "F03_SPACES": re.compile(r'\s+'),
        "F04_GERMAN_UMLAUTS": re.compile(r'[äöüÄÖÜß]'),
        "F05_LOWERCASE_IN_ID": re.compile(r'[a-z]'),
        "F06_NON_ASCII": re.compile(r'[^\x00-\x7F]')
    }

    def validate_identifier(self, identifier: str) -> Dict[str, Any]:
        violations = []
        
        # Rule 1: B6_ Prefix Check
        if not identifier.startswith("B6_"):
            violations.append("R01_FAIL: Fehlendes 'B6_'-Präfix.")
            
        # Rule 2: UPPER_SNAKE_CASE Check
        if not re.match(r'^B6_[A-Z0-9\_]+$', identifier):
            violations.append("R02_FAIL: Ungültiges Format (erfordert UPPER_SNAKE_CASE).")
            
        # Rule 3 & 4: Forbidden Chars Checks
        for f_code, pattern in self.FORBIDDEN_PATTERNS.items():
            if f_code == "F05_LOWERCASE_IN_ID" and not identifier.startswith("B6_"):
                continue
            if pattern.search(identifier):
                violations.append(f"{f_code}: Verbotene Zeichenklasse erkannt.")
                
        is_valid = len(violations) == 0
        return {
            "identifier": identifier,
            "valid": is_valid,
            "violations": violations
        }

    def run_suite(self, test_identifiers: List[str]) -> Dict[str, Any]:
        results = [self.validate_identifier(ident) for ident in test_identifiers]
        passed = sum(1 for r in results if r["valid"])
        failed = len(results) - passed
        return {
            "total_tested": len(results),
            "passed": passed,
            "failed": failed,
            "pass_rate_pct": round((passed / len(results)) * 100, 2) if results else 0.0,
            "details": results
        }

if __name__ == "__main__":
    validator = B6CALMValidator()
    test_cases = [
        "B6_SYS_CORE_ENGINE",
        "B6_SAEULE_TRIX",
        "B6_STRAND_CALM",
        "B6_EBPF_KRAKENGUARD_SHIELD",
        "b6_sys_invalid_lowercase", # F05 & R01/R02 Fail
        "B6_SYS_Ω_OMEGA",           # F01 & F06 Fail
        "B6_SYS_TEST+FAIL",         # F02 Fail
        "B6_SYS_UMLAUT_ÄNDERUNG"    # F04 Fail
    ]
    report = validator.run_suite(test_cases)
    print(f"=== B6 CALM VALIDATION SUITE REPORT ===")
    print(f"Total: {report['total_tested']} | Passed: {report['passed']} | Failed: {report['failed']} | Success Rate: {report['pass_rate_pct']}%")
    print("-" * 50)
    for detail in report["details"]:
        status = "PASSED" if detail["valid"] else "FAILED"
        print(f"[{status}] {detail['identifier']}")
        if not detail["valid"]:
            for v in detail["violations"]:
                print(f" └── {v}")
