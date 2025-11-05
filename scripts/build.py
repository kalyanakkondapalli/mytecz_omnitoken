#!/usr/bin/env python3
"""
Build script for MyTecZ OmniToken package.

This script automates the building, testing, and publishing process
for the MyTecZ OmniToken library to PyPI.

Usage:
    python scripts/build.py [command]
    
Commands:
    clean       - Clean build artifacts
    build       - Build distribution packages
    test        - Run test suite
    check       - Check package validity
    upload-test - Upload to TestPyPI
    upload      - Upload to PyPI
    all         - Run all steps (clean, build, test, check)
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path
from typing import List, Optional


class BuildManager:
    """Manages the build process for the package."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize build manager.
        
        Args:
            project_root: Path to project root directory
        """
        self.project_root = project_root or Path(__file__).parent.parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.egg_info_dir = self.project_root / "mytecz_omnitoken.egg-info"
    
    def run_command(self, command: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """
        Run a shell command.
        
        Args:
            command: Command to run as list of strings
            check: Whether to check return code
            
        Returns:
            CompletedProcess result
        """
        print(f"Running: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                check=check,
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                print(result.stdout)
            
            if result.stderr and result.returncode != 0:
                print(f"Error: {result.stderr}", file=sys.stderr)
            
            return result
            
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            if e.stdout:
                print("STDOUT:", e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            raise
    
    def clean(self) -> None:
        """Clean build artifacts and temporary files."""
        print("🧹 Cleaning build artifacts...")
        
        # Directories to remove
        dirs_to_clean = [
            self.dist_dir,
            self.build_dir,
            self.egg_info_dir,
            self.project_root / "__pycache__",
            self.project_root / "omnitoken" / "__pycache__"
        ]
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                print(f"  Removing: {dir_path}")
                shutil.rmtree(dir_path)
        
        # Find and remove all __pycache__ directories
        for pycache in self.project_root.rglob("__pycache__"):
            if pycache.is_dir():
                print(f"  Removing: {pycache}")
                shutil.rmtree(pycache)
        
        # Find and remove all .pyc files
        for pyc_file in self.project_root.rglob("*.pyc"):
            if pyc_file.is_file():
                print(f"  Removing: {pyc_file}")
                pyc_file.unlink()
        
        print("✅ Clean completed")
    
    def install_build_dependencies(self) -> None:
        """Install build dependencies."""
        print("📦 Installing build dependencies...")
        
        dependencies = [
            "build",
            "twine", 
            "pytest",
            "pytest-cov",
            "wheel",
            "setuptools"
        ]
        
        self.run_command([sys.executable, "-m", "pip", "install", "--upgrade"] + dependencies)
        print("✅ Build dependencies installed")
    
    def build_package(self) -> None:
        """Build the distribution packages."""
        print("🔨 Building distribution packages...")
        
        # Create dist directory
        self.dist_dir.mkdir(exist_ok=True)
        
        # Build using python -m build
        self.run_command([sys.executable, "-m", "build"])
        
        # List built files
        if self.dist_dir.exists():
            built_files = list(self.dist_dir.glob("*"))
            if built_files:
                print("📦 Built packages:")
                for file in built_files:
                    size = file.stat().st_size / 1024  # Size in KB
                    print(f"  {file.name} ({size:.1f} KB)")
            else:
                print("⚠️  No packages found in dist directory")
        
        print("✅ Build completed")
    
    def run_tests(self) -> None:
        """Run the test suite."""
        print("🧪 Running test suite...")
        
        # Check if pytest is available
        try:
            self.run_command([sys.executable, "-m", "pytest", "--version"])
        except subprocess.CalledProcessError:
            print("Installing pytest...")
            self.run_command([sys.executable, "-m", "pip", "install", "pytest"])
        
        # Run tests with coverage
        test_command = [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short"
        ]
        
        # Add coverage if available
        try:
            self.run_command([sys.executable, "-m", "pytest_cov", "--version"], check=False)
            test_command.extend(["--cov=omnitoken", "--cov-report=term-missing"])
        except subprocess.CalledProcessError:
            pass  # Coverage not available, skip it
        
        self.run_command(test_command)
        print("✅ Tests completed")
    
    def check_package(self) -> None:
        """Check package validity and metadata."""
        print("🔍 Checking package validity...")
        
        # Check with twine
        dist_files = list(self.dist_dir.glob("*"))
        if not dist_files:
            raise RuntimeError("No distribution files found. Run 'build' first.")
        
        # Check distribution files
        self.run_command([sys.executable, "-m", "twine", "check"] + [str(f) for f in dist_files])
        
        # Check if package can be imported
        print("Testing package import...")
        test_import_code = """
try:
    import omnitoken
    from omnitoken import OmniToken
    print(f"✅ Package import successful. Version: {omnitoken.__version__}")
except ImportError as e:
    print(f"❌ Package import failed: {e}")
    exit(1)
"""
        
        self.run_command([sys.executable, "-c", test_import_code])
        print("✅ Package check completed")
    
    def upload_to_testpypi(self) -> None:
        """Upload package to TestPyPI."""
        print("📤 Uploading to TestPyPI...")
        
        dist_files = list(self.dist_dir.glob("*"))
        if not dist_files:
            raise RuntimeError("No distribution files found. Run 'build' first.")
        
        # Upload to TestPyPI
        upload_command = [
            sys.executable, "-m", "twine", "upload",
            "--repository", "testpypi",
            "--verbose"
        ] + [str(f) for f in dist_files]
        
        print("Note: You'll need to enter your TestPyPI credentials.")
        self.run_command(upload_command)
        
        print("✅ Upload to TestPyPI completed")
        print("🔗 Check your package at: https://test.pypi.org/project/mytecz-omnitoken/")
    
    def upload_to_pypi(self) -> None:
        """Upload package to PyPI."""
        print("📤 Uploading to PyPI...")
        
        # Confirm with user
        response = input("Are you sure you want to upload to PyPI? This cannot be undone. (yes/no): ")
        if response.lower() != "yes":
            print("Upload cancelled.")
            return
        
        dist_files = list(self.dist_dir.glob("*"))
        if not dist_files:
            raise RuntimeError("No distribution files found. Run 'build' first.")
        
        # Upload to PyPI
        upload_command = [
            sys.executable, "-m", "twine", "upload",
            "--verbose"
        ] + [str(f) for f in dist_files]
        
        print("Note: You'll need to enter your PyPI credentials.")
        self.run_command(upload_command)
        
        print("✅ Upload to PyPI completed")
        print("🔗 Check your package at: https://pypi.org/project/mytecz-omnitoken/")
    
    def run_all(self) -> None:
        """Run all build steps."""
        print("🚀 Running complete build process...")
        
        try:
            self.install_build_dependencies()
            self.clean()
            self.build_package()
            self.run_tests()
            self.check_package()
            
            print("\n" + "="*60)
            print("🎉 BUILD SUCCESSFUL!")
            print("="*60)
            print("Next steps:")
            print("  1. Test upload: python scripts/build.py upload-test")
            print("  2. Production upload: python scripts/build.py upload")
            print("="*60)
            
        except Exception as e:
            print("\n" + "="*60)
            print("❌ BUILD FAILED!")
            print("="*60)
            print(f"Error: {e}")
            print("="*60)
            sys.exit(1)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Build script for MyTecZ OmniToken",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/build.py clean          # Clean build artifacts
  python scripts/build.py build          # Build distribution
  python scripts/build.py test           # Run tests
  python scripts/build.py all            # Run complete build process
  python scripts/build.py upload-test    # Upload to TestPyPI
  python scripts/build.py upload         # Upload to PyPI
        """
    )
    
    parser.add_argument(
        "command",
        choices=["clean", "build", "test", "check", "upload-test", "upload", "all"],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    # Create build manager
    builder = BuildManager()
    
    # Execute command
    command_map = {
        "clean": builder.clean,
        "build": builder.build_package,
        "test": builder.run_tests,
        "check": builder.check_package,
        "upload-test": builder.upload_to_testpypi,
        "upload": builder.upload_to_pypi,
        "all": builder.run_all
    }
    
    try:
        command_map[args.command]()
    except KeyboardInterrupt:
        print("\n⚠️  Build interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()