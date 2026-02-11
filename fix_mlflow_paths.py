import os

def fix_mlflow_paths():
    project_root = os.getcwd().replace('\\', '/')
    mlruns_dir = os.path.join(os.getcwd(), "mlruns")
    
    print(f"Searching for meta.yaml files in: {mlruns_dir}")
    print(f"New project root: {project_root}")
    
    count = 0
    for root, dirs, files in os.walk(mlruns_dir):
        for file in files:
            if file == "meta.yaml":
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                new_lines = []
                modified = False
                
                for line in lines:
                    if line.strip().startswith("artifact_location:"):
                        # Check if it has the old path specific to 'jayan' or just needs update
                        # We will replace the entire prefix up to 'mlruns' with the current project path
                        
                        parts = line.split("file:///", 1)
                        if len(parts) == 2:
                            # Extract everything after 'mlruns'
                            current_val = parts[1].strip()
                            if "mlruns" in current_val:
                                # Find where mlruns starts
                                # Handle case mixing / and \
                                current_val_norm = current_val.replace('\\', '/')
                                idx = current_val_norm.find('mlruns')
                                suffix = current_val_norm[idx:]
                                
                                new_uri = f"file:///{project_root}/{suffix}"
                                new_line = f"artifact_location: {new_uri}\n"
                                
                                if new_line != line:
                                    new_lines.append(new_line)
                                    modified = True
                                else:
                                    new_lines.append(line)
                            else:
                                new_lines.append(line)
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)
                
                if modified:
                    print(f"Updating {file_path}")
                    with open(file_path, 'w') as f:
                        f.writelines(new_lines)
                    count += 1
    
    print(f"Fixed {count} meta.yaml files.")

if __name__ == "__main__":
    fix_mlflow_paths()
