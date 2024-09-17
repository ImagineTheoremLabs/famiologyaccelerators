import os

def find_sqlite_databases(directory):
    """
    Find all SQLite database files with .sqlite or .db extension in the specified directory.
    
    Args:
        directory (str): The directory to search in.

    Returns:
        List of paths to database files.
    """
    sqlite_databases = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.sqlite') or file.endswith('.db'):
                sqlite_databases.append(os.path.join(root, file))
    
    return sqlite_databases


def returnAvailabledatabases():
    # Specify the directory you want to search
    directory_to_search = '.'

    # Get the list of database files
    database_files = find_sqlite_databases(directory_to_search)

    # Print the database files
    if database_files:
        print("Found the following SQLite database files:")
        database_names = [os.path.splitext(os.path.basename(db))[0] for db in database_files]
        database_dict = {file.split('/')[-1].split('.')[0]: file for file in database_files}
        return database_dict

        # keys_list = list(database_dict.keys())
        # print("keys_list", keys_list)


        # print("file_dict", database_dict)

        # for db_file in database_names:
        #     print(db_file)

if __name__ == "__main__":
    print("dict", returnAvailabledatabases())
