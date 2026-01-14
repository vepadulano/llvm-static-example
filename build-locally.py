#!/usr/bin/env python3
"""
This script is for conda-forge feedstock local builds.
It sets up the necessary environment and runs conda-build.
"""
import os
import sys
import subprocess
from pathlib import Path


def setup_environment():
    """Setup conda-forge environment variables."""
    os.environ["CONFIG"] = "linux_64_"
    os.environ["UPLOAD_PACKAGES"] = "False"
    os.environ["CI"] = "False"


def main():
    """Run local conda build."""
    setup_environment()
    
    recipe_dir = Path(__file__).parent / "recipe"
    
    if not recipe_dir.exists():
        # If no recipe subdirectory, assume current directory is recipe
        recipe_dir = Path(__file__).parent
    
    print(f"Building recipe in: {recipe_dir}")
    
    cmd = [
        "conda",
        "build",
        str(recipe_dir),
        "--no-anaconda-upload",
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Build successful!")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with exit code {e.returncode}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
