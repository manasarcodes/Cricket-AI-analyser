import os

folder_path = r'F:\manasa-backup_21-07-2025\Projects\Cricket ai analyser'
files = os.listdir(folder_path)

print("Files found in this folder:")
for file in files:
    print(f"- {file}")