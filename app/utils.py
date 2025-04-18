import pickle

def save_to_file(data, file_path):
    """Save data to a file."""
    try:
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def load_from_file(file_path):
    """Load data from a file."""
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}