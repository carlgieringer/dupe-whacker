import os
import sys

# Returns all paths within base_dir that would conflict
# in a case-insensitive context
def find_conflicts(base_dir):
    # Contains paths found to conflict in a case-insensitive
    # context
    conflicting_paths = set()

    find_conflicts_backend(base_dir, conflicting_paths)

    return conflicting_paths

# Adds to conflicting_paths all paths within base_dir that would conflict
# in a case-insensitive context
def find_conflicts_backend(base_dir, conflicting_paths):
    # Maps case-insensitive paths to the first path
    # found that produced the key.  Used to determine
    # if later paths would conflict in a case-insensitive
    # context.
    entries = dict()

    file_names = os.listdir(base_dir)
    subdirs = []
    for file_name in file_names:
        path = os.path.join(base_dir, file_name)
        key = make_key(path)

        conflicting_path = entries.get(key, None)
        if conflicting_path is None:
            entries[key] = path
        else:
            if not conflicting_path in conflicting_paths:
                conflicting_paths.add(conflicting_path)
            conflicting_paths.add(path)

        if os.path.isdir(path):
            subdirs.append(path)

    for subdir in subdirs:
        find_conflicts_backend(subdir, conflicting_paths)

def make_key(path):
    return path.lower()

def print_conflicts(conflicting_paths):
    count = len(conflicting_paths)
    if count < 1:
        print("No conflicts")
    else:
        print("{count} conflicting paths:".format(count=count))
        sorted_paths = sorted(conflicting_paths, key=lambda s: s.lower())
        for path in sorted_paths:
            print(path)

if __name__ == "__main__":
    path = None
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

    print("Finding paths that would conflict in a case-insensitive context.")
    print("Looking in: {base_dir}".format(base_dir=path))

    conflicting_paths = find_conflicts(path)

    print_conflicts(conflicting_paths)

    sys.exit(0)