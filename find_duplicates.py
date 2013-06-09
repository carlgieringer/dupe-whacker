import os
import sys
# sys.path.append('/Volumes/Spin/Users/tech/Development/FileUtils/python-sha3/build/lib.macosx-10.4-x86_64-2.7/')
# try:
#     import sha3
# except ImportError as ex:
#     print(ex)
#     print("(sha3 must be in LD_LIBRARY_PATH env variable)")
#     print("(maybe export LD_LIBRARY_PATH=/Volumes/Spin/Users/tech/Development/FileUtils/python-sha3/build/lib.macosx-10.4-x86_64-2.7/)")
import hashlib

# Maps a file size to file path(s)
paths_by_size = dict()

# Maps file paths to file hashes
hash_by_path = dict()

# Returns a map of hashes to file paths sharing that hash
def find_duplicates(base_dir):
    # Maps hashes to paths that have that hash
    duplicate_paths_by_hash = dict()

    find_duplicates_backend(base_dir, duplicate_paths_by_hash)

    return duplicate_paths_by_hash

# Modifies duplicate_paths_by_hash to contain mappings from hash to
# file path of any files within base_dir that have duplicate hashes
# as other files within base_dir or already in duplicate_paths_by_hash
# 
# TODO use os.walk
# http://docs.python.org/2/library/os.html#os.walk
def find_duplicates_backend(base_dir, duplicate_paths_by_hash):

    subdirs = []
    file_paths = []

    # Look at the directory's contents and split them into files and sub-directories
    content_paths = [os.path.join(base_dir, content) for content in os.listdir(base_dir)]
    for content_path in content_paths:
        if os.path.isdir(content_path):
            subdirs.append(content_path)
        else:
            file_paths.append(content_path)

    for file_path in file_paths:
        file_size = get_size(file_path)

        # First see if any previous paths had the same file size; only compare
        # hashes if files have the same size.
        # It is cheaper to look at file size first, since that can be read
        # from the file system whereas computing the hash requires reading the
        # entire file and then computing the hash.
        same_size_paths = paths_by_size.get(file_size, None)
        if same_size_paths is None:
            # No need to compute the hash
            paths_by_size[file_size] = [file_path]
        else:
            file_hash = make_hash(file_path)
            hash_by_path[file_path] = file_hash

            for same_size_path in same_size_paths:
                # The first path having a particular size will not have had its hash compute
                same_size_hash = hash_by_path.get(same_size_path, None)
                if same_size_hash is None:
                    same_size_hash = make_hash(same_size_path)
                    hash_by_path[same_size_path] = same_size_hash
                if file_hash == same_size_hash:
                    duplicate_paths = duplicate_paths_by_hash.get(file_hash, None)
                    if duplicate_paths is None:
                        duplicate_paths = [same_size_path, file_path]
                        duplicate_paths_by_hash[file_hash] = duplicate_paths
                    else:
                        if same_size_path not in duplicate_paths:
                            duplicate_paths.append(same_size_path)
                        duplicate_paths.append(file_path)
            same_size_paths.append(file_path)

    for subdir in subdirs:
        find_duplicates_backend(subdir, duplicate_paths_by_hash)

def get_size(file_path):
    # statinfo = os.stat(file_path)
    # return statinfo.st_size
    return os.path.getsize(file_path)

# def make_hash(file_path):
#     with file(file_path) as f:
#         file_bytes = f.read()
#     hasher = SHA3512()
#     hasher.update(file_bytes)
#     return hasher.hexdigest()

def make_hash(file_path):
    with file(file_path) as f:
        file_bytes = f.read()
    hasher = hashlib.new('sha1')
    hasher.update(file_bytes)
    return hasher.hexdigest()

def print_duplicates(duplicate_paths_by_hash):
    count = len(duplicate_paths_by_hash.values())
    if count < 1:
        print("No duplicates")
    else:
        print("{count} duplicate files:".format(count=count))
        for duplicate_hash, duplicate_paths in duplicate_paths_by_hash.items():
            sorted_paths = sorted(duplicate_paths, key=lambda s: s.lower())
            for path in sorted_paths:
                print("{hash} {path}".format(hash=duplicate_hash, path=path))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1]
        if not os.path.exists(path):
            print(""""{path}" is not a valid path""".format(path=path))
            sys.exit(1)
    elif len(sys.argv) > 2:
        script_path = os.path.realpath(__file__)
        script_dir, script_name = os.path.split(script_path)
        print("usage: {file_name} [path (= current working directory)]".format(file_name=script_name))
        sys.exit(1)
    else:
        path = os.getcwd()

    print("Finding binary duplicate files.")
    print("Looking in: {base_dir}".format(base_dir=path))

    duplicate_paths_by_hash = find_duplicates(path)

    print_duplicates(duplicate_paths_by_hash)

    sys.exit(0)