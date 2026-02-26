import os
import shutil
import kagglehub

def download_titanic_dataset():
    # 1. Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    target_file = os.path.join(data_dir, "titanic.csv")

    # 2. Check if dataset already exists
    if os.path.exists(target_file):
        print(f"Titanic dataset already exists at: {target_file}")
        return

    print("Dataset missing. Downloading from Kaggle...")

    try:
        # 3. Download the latest version from Kaggle
        # Using a reliable public mirror of the Titanic dataset
        path = kagglehub.dataset_download("yasserh/titanic-dataset")
        
        # 4. Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)

        # 5. Move the specific CSV file to your backend/data folder
        # Kagglehub downloads to a cache folder, so we move it to your project
        source_file = os.path.join(path, "Titanic-Dataset.csv")
        shutil.move(source_file, target_file)
        
        print(f"Successfully downloaded and moved to: {target_file}")

    except Exception as e:
        print(f"[Error] Unable to download dataset: {e}")

if __name__ == "__main__":
    download_titanic_dataset()