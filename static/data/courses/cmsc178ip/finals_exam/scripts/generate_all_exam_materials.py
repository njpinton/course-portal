#!/usr/bin/env python3
"""
CMSC 178IP Finals Exam - Material Generation Script
Generates all images and datasets needed for the practical finals exam.

Run this script from the finals_exam directory:
    python scripts/generate_all_exam_materials.py
"""

import subprocess
import sys
import os
from pathlib import Path

def run_script(script_path, description):
    """Run a generation script and report status."""
    print(f"\n{'='*60}")
    print(f"Generating: {description}")
    print(f"Script: {script_path}")
    print('='*60)

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
            if result.stdout:
                print(result.stdout[:500])
        else:
            print(f"❌ FAILED: {description}")
            print(f"Error: {result.stderr[:500]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {description}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

    return True

def main():
    # Get the finals_exam directory
    script_dir = Path(__file__).parent
    finals_dir = script_dir.parent

    print("\n" + "="*60)
    print("CMSC 178IP Finals Exam - Material Generator")
    print("="*60)

    scripts = [
        ("part0_fundamentals/scripts/generate_fundamentals.py", "Part 0: Image Fundamentals"),
        ("part1_cnn_analysis/scripts/generate_cnn_materials.py", "Part 1: CNN Analysis Materials"),
        ("part2_segmentation/scripts/generate_segmentation_data.py", "Part 2: Segmentation Dataset"),
        ("part3_generative/scripts/generate_generative_materials.py", "Part 3: Generative Model Materials"),
        ("bonus_application/scripts/generate_bonus_materials.py", "Bonus: Application Materials"),
    ]

    results = []
    for script_rel, description in scripts:
        script_path = finals_dir / script_rel
        if script_path.exists():
            success = run_script(str(script_path), description)
            results.append((description, success))
        else:
            print(f"\n⚠️  Script not found: {script_path}")
            results.append((description, False))

    # Summary
    print("\n" + "="*60)
    print("GENERATION SUMMARY")
    print("="*60)
    for desc, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {desc}")

    successful = sum(1 for _, s in results if s)
    print(f"\n{successful}/{len(results)} scripts completed successfully")

    if successful == len(results):
        print("\n🎉 All materials generated! Ready for exam deployment.")
    else:
        print("\n⚠️  Some materials failed to generate. Check errors above.")

if __name__ == "__main__":
    main()
