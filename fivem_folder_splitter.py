import os
import shutil
from pathlib import Path

def get_file_size(file_path):
    """Get size of file in bytes."""
    return os.path.getsize(file_path)

def get_folder_contents(folder_path):
    """Get all files in folder with their sizes."""
    files_info = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, folder_path)
            size = get_file_size(full_path)
            files_info.append((full_path, relative_path, size))
    return files_info

def split_folder(source_folder, num_parts=2):
    """Split folder contents into specified number of parts."""
    # Get all files and their sizes
    files_info = get_folder_contents(source_folder)
    
    if not files_info:
        print(f"No files found in {source_folder}")
        return
    
    # Calculate total size and target size per part
    total_size = sum(info[2] for info in files_info)
    target_size_per_part = total_size / num_parts
    
    # Sort files by size (largest first) to help with even distribution
    files_info.sort(key=lambda x: x[2], reverse=True)
    
    # Create output folders
    source_name = os.path.basename(source_folder)
    parts = [[] for _ in range(num_parts)]
    parts_sizes = [0] * num_parts
    
    # Distribute files
    for file_info in files_info:
        # Find the part with smallest current size
        target_part = min(range(num_parts), key=lambda i: parts_sizes[i])
        parts[target_part].append(file_info)
        parts_sizes[target_part] += file_info[2]
    
    # Create output folders and copy files
    for i, part_files in enumerate(parts):
        output_folder = f"{source_folder}_part{i + 1}"
        print(f"\nCreating {output_folder}")
        print(f"Size: {parts_sizes[i] / (1024 * 1024 * 1024):.2f} GB")
        
        if not part_files:
            continue
            
        for orig_path, rel_path, _ in part_files:
            # Create target path
            target_path = os.path.join(output_folder, rel_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # Copy file
            shutil.copy2(orig_path, target_path)
            print(f"Copied: {rel_path}")

def main():
    while True:
        folder_path = input("Enter the path to the FiveM resource folder to split (or 'quit' to exit): ").strip()
        
        if folder_path.lower() == 'quit':
            break
            
        if not os.path.exists(folder_path):
            print("Error: Folder does not exist!")
            continue
            
        try:
            num_parts = int(input("Enter number of parts to split into (default: 2): ") or 2)
            if num_parts < 2:
                print("Number of parts must be at least 2")
                continue
        except ValueError:
            print("Please enter a valid number")
            continue
            
        print(f"\nSplitting folder: {folder_path}")
        split_folder(folder_path, num_parts)
        print("\nSplit complete!")

if __name__ == "__main__":
    main()
