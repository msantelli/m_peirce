#!/usr/bin/env python3
"""
upload_to_huggingface.py

Utility to upload logical reasoning datasets to HuggingFace Hub.
"""

import os
from pathlib import Path
from typing import Optional

def upload_dataset(dataset_path: Path, 
                  repo_name: str,
                  username: str,
                  token: Optional[str] = None,
                  private: bool = False) -> None:
    """
    Upload a dataset to HuggingFace Hub.
    
    Args:
        dataset_path: Path to dataset directory
        repo_name: Name for the repository (e.g., "logical-reasoning-arguments")
        username: Your HuggingFace username
        token: HuggingFace API token (or set HF_TOKEN environment variable)
        private: Whether to make the dataset private
    """
    
    try:
        from huggingface_hub import HfApi, create_repo, upload_folder
    except ImportError:
        print("❌ Error: huggingface_hub not installed")
        print("Install with: pip install huggingface_hub")
        return
    
    if not dataset_path.exists():
        print(f"❌ Error: Dataset directory not found: {dataset_path}")
        return
    
    # Check for required files
    required_files = ['train.jsonl', 'test.jsonl', 'README.md']
    missing_files = []
    
    for file in required_files:
        if not (dataset_path / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Error: Missing required files: {missing_files}")
        print("Generate README.md with: python create_hf_dataset_card.py")
        return
    
    # Setup API
    api = HfApi()
    
    if token:
        api.token = token
    elif 'HF_TOKEN' in os.environ:
        api.token = os.environ['HF_TOKEN']
    else:
        print("❌ Error: No HuggingFace token provided")
        print("Either:")
        print("  1. Pass --token YOUR_TOKEN")
        print("  2. Set environment variable: export HF_TOKEN=your_token")
        print("  3. Run: huggingface-cli login")
        return
    
    repo_id = f"{username}/{repo_name}"
    
    print(f"🚀 Uploading dataset to: {repo_id}")
    print(f"📁 Source: {dataset_path}")
    print(f"🔒 Private: {private}")
    
    try:
        # Create repository
        print("Creating repository...")
        create_repo(
            repo_id=repo_id,
            repo_type="dataset", 
            private=private,
            exist_ok=True
        )
        
        # Upload files
        print("Uploading files...")
        upload_folder(
            folder_path=str(dataset_path),
            repo_id=repo_id,
            repo_type="dataset",
            ignore_patterns=["*.pyc", "__pycache__", ".git"]
        )
        
        print(f"✅ Successfully uploaded to: https://huggingface.co/datasets/{repo_id}")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")


def main():
    """CLI interface for uploading datasets."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Upload logical reasoning datasets to HuggingFace Hub")
    parser.add_argument("dataset_path", help="Path to dataset directory")
    parser.add_argument("repo_name", help="Repository name (e.g., 'logical-reasoning-arguments')")
    parser.add_argument("username", help="Your HuggingFace username")
    parser.add_argument("--token", help="HuggingFace API token")
    parser.add_argument("--private", action="store_true", help="Make dataset private")
    
    args = parser.parse_args()
    
    dataset_path = Path(args.dataset_path)
    
    upload_dataset(
        dataset_path=dataset_path,
        repo_name=args.repo_name, 
        username=args.username,
        token=args.token,
        private=args.private
    )


if __name__ == "__main__":
    main()