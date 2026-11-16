from pathlib import Path
import subprocess
import sys

DATA_DIR = Path(__file__).resolve().parent
PROJECT_DIR = DATA_DIR.parent

SCRIPTS = [
    "clean_data.py",
    "validate_clean_data.py",
    "verify_rbi_extraction.py",
    "verify_upi_sources.py",
]


def run_script(script):
    path = DATA_DIR / script

    print(f"\n{'=' * 65}")
    print(f"RUNNING: {script}")
    print("=" * 65, flush=True)

    subprocess.run(
        [sys.executable, str(path)],
        cwd=PROJECT_DIR,
        check=True,
    )

    print(f"\nSUCCESS: {script}")


def main():
    try:
        for script in SCRIPTS:
            run_script(script)

        print("\n" + "=" * 65)
        print("DATA PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 65)

    except subprocess.CalledProcessError as error:
        print(f"\nPIPELINE FAILED: {error}")
        sys.exit(error.returncode)


if __name__ == "__main__":
    main()
