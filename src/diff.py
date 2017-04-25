# import modules
import os
import git
import re

## Module Constants
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def parse_diff(path, branch='master'):
    """
    Returns a generator which iterates through all commits of
    the repository located in the given path for the given branch. It yields
    file diff information to show a timeseries of file changes.
    """

    # Create the repository, raises an error if it isn't one.
    repo = git.Repo(path)
    r_git = repo.git
    # t = repo.head.commit.tree
    # print(repo.git.diff('HEAD~1'))
    temp_commit = {
        'commit': None
    }

    # Iterate through every commit for the given branch in the repository
    for commit in repo.iter_commits(branch):
        # Determine the parent of the commit to diff against.
        # If no parent, this is the first commit, so use empty tree.
        # Then create a mapping of path to diff for each file changed.
        
        parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
        diffs  = {
            diff.a_path: diff for diff in commit.diff(parent)
        }

        # r_git.diff(temp_commit['commit'], commit)
        # print(r_git.diff(temp_commit['commit'], commit))
        raw_diff = r_git.diff(temp_commit['commit'], commit)
        parsed_diff = parse_raw_diff(raw_diff)

        temp_commit['commit'] = commit
        # print(temp_commit['commit'])
        
        # The stats on the commit is a summary of all the changes for this
        # commit, we'll iterate through it to get the information we need.
        for objpath, stats in commit.stats.files.items():

            # Select the diff for the path in the stats
            diff = diffs.get(objpath)

            # If the path is not in the dictionary, it's because it was
            # renamed, so search through the b_paths for the current name.
            if not diff:
                for diff in diffs.values():
                    if diff.b_path == path and diff.renamed:
                        break

            # Update the stats with the additional information
            stats.update({
                'object': os.path.join(path, objpath),
                'commit': commit.hexsha,
                'author': commit.author.email,
                'timestamp': commit.authored_datetime.strftime(DATE_TIME_FORMAT),
                'type': diff_type(diff),
            })

            yield stats

def diff_type(diff):
    """
    Determines the type of the diff by looking at the diff flags.
    """

    if diff.renamed: return 'R'
    if diff.deleted_file: return 'D'
    if diff.new_file: return 'A'
    return 'M'

def parse_raw_diff(raw_diff):
    """
    Parse raw diff from git, identify added, deleted, changed lines
    """

    raw_diff_lines = raw_diff.splitlines()
    # print(raw_diff)
    # print(raw_diff_lines)
    # temp Dict to hold meta info to identify different types of lines ie: added, deleted
    temp_data = {
        'diff': False,
        'line_data': None, # at runtime this will be replaced by a Dict contains : no, start, end
        'lines': None # at runtime this will be replaced by a Dict
    }

    current_line = 0
    for line in raw_diff_lines:
        if(line.startswith('--- ')):
            temp_data['diff'] = True
            temp_data['line_data'] = {
                'no': 2
            }
        elif(line.startswith('+++ ')):
            temp_data['diff'] = True
            temp_data['line_data'] = {
                'no': 2
            }
    # pattern = re.compile('diff --git')
    # match = bool(pattern.match(raw_diff))
    # if match:
    #     print('yeah')
    # else:
    #     print('nah')
    return raw_diff

for diff_info in parse_diff('/home/rajika/react-scaffolder'):
    print(diff_info)