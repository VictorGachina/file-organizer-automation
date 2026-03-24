import os
import shutil
from pathlib import Path

def organize_files(directory_path):
    """
    Automatically organizes files in a directory into subfolders
    based on their file extensions.
    """
    # Define file categories
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
        'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls', '.pptx', '.ppt'],
        'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
        'Code': ['.py', '.js', '.html', '.css', '.json', '.xml', '.cpp', '.c'],
        'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.wmv'],
        'Music': ['.mp3', '.wav', '.flac', '.aac'],
        'Spreadsheets': ['.csv', '.xlsx', '.xls', '.ods']
    }
    
    # Create folders if they don't exist
    for folder in file_types.keys():
        folder_path = os.path.join(directory_path, folder)
        os.makedirs(folder_path, exist_ok=True)
    
    # Move files
    moved_count = 0
    skipped_files = []
    
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        
        # Skip folders
        if os.path.isdir(file_path):
            continue
            
        # Get file extension
        _, ext = os.path.splitext(file)
        ext = ext.lower()
        
        # Find matching folder and move
        moved = False
        for folder, extensions in file_types.items():
            if ext in extensions:
                destination = os.path.join(directory_path, folder, file)
                # Handle duplicate filenames
                if os.path.exists(destination):
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(os.path.join(directory_path, folder, f"{base}_{counter}{ext}")):
                        counter += 1
                    destination = os.path.join(directory_path, folder, f"{base}_{counter}{ext}")
                
                shutil.move(file_path, destination)
                moved_count += 1
                print(f"✅ Moved: {file} → {folder}/")
                moved = True
                break
        
        if not moved:
            skipped_files.append(file)
            print(f"⚠️ Skipped: {file} (unknown file type)")
    
    # Summary
    print("\n" + "="*40)
    print(f"📊 SUMMARY")
    print("="*40)
    print(f"Total files organized: {moved_count}")
    
    if skipped_files:
        print(f"Files skipped ({len(skipped_files)}):")
        for f in skipped_files:
            print(f"  - {f}")
    
    print(f"\n✨ Organization complete!")

def main():
    import sys
    
    print("📁 FILE ORGANIZER AUTOMATION")
    print("-" * 30)
    
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = input("Enter directory path to organize: ").strip()
    
    # Remove quotes if present
    target_dir = target_dir.strip('"').strip("'")
    
    # Expand user home directory if ~ is used
    target_dir = os.path.expanduser(target_dir)
    
    if os.path.exists(target_dir):
        print(f"\n📂 Target: {target_dir}")
        confirm = input("Proceed with organization? (y/n): ").lower()
        if confirm == 'y':
            organize_files(target_dir)
        else:
            print("❌ Operation cancelled.")
    else:
        print(f"❌ Directory does not exist: {target_dir}")

if __name__ == "__main__":
    main()
