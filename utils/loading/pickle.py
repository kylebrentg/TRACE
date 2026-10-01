import pickle


def load_pickle_file(file_path_to_load: str) -> list:
    with open(file_path_to_load, "rb") as f:
        return pickle.load(f)

def save_record_to_pickle(file_path_to_save: str, records: list) -> str:
    with open(file_path_to_save, "wb") as f:
        pickle.dump(records, f)

    return file_path_to_save