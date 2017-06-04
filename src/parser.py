# import modules
import os
import git
import re

## Module Constants
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


class Parser:

    def parse_diff(self, path, branch='master'):
        """
        Returns a generator which iterates through all commits of
        the repository located in the given path for the given branch. It yields
        file diff information to show a timeseries of file changes.
        """

        # Create the repository, raises an error if it isn't one.
        repo = git.Repo(path)
        r_git = repo.git
        # t = repo.head.commit.tree
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
            raw_diff = r_git.diff(temp_commit['commit'], commit)
            # print(raw_diff)
            parsed_diff = self.parse_raw_diff(raw_diff)
            # print(parsed_diff)
            temp_commit['commit'] = commit
            
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
                for indv_diff in parsed_diff:
                    stats.update({
                        'object': os.path.join(path, objpath),
                        'commit': commit.hexsha,
                        'author': commit.author.email,
                        'file_name': indv_diff['file_name'],
                        'added_lines': indv_diff['added_lines'],
                        'deleted_lines': indv_diff['deleted_lines'],
                        'timestamp': commit.authored_datetime.strftime(DATE_TIME_FORMAT),
                        'type': self.diff_type(diff),
                    })

                yield stats

    def diff_type(self, diff):
        """
        Determines the type of the diff by looking at the diff flags.
        """

        if diff.renamed: return 'R'
        if diff.deleted_file: return 'D'
        if diff.new_file: return 'A'
        return 'M'

    def parse_raw_diff(self, raw_diff):
        """
        Parse raw diff from git, identify added, deleted, changed lines
        """
        raw_diff_lines = raw_diff.splitlines()
        # structures to hold values at runtime
        diffs_data = []

        file_names = []
        deleted_lines = []
        added_lines = []
        last_deleted_line = 0
        last_added_line = 0
        current_line = 0
        
        current_file = None

        glob_from_line = 0
        new_file = False

        temp_count = 0

        from_line = 0
        from_count = 0
        to_line = 0
        to_count = 0

        for line in raw_diff_lines:
            # print(">>>>>> LINE"  + line + "line number " + str(current_line))
            temp_count = temp_count + 1

            if(line.startswith('diff --git ')):
                is_diff = False
                # last_deleted_line = 0
                glob_from_line = 0
                last_added_line = 0
                current_line = 0
                glob_from_line = 0
                continue
            if(line.startswith('---')):
                re_compile = re.compile('--- a/(\w+)?')
                matches = re_compile.findall(line)
                str_split = line.split('--- a/');

                for file_name_match in str_split:
                    file_names.append(file_name_match)
                    diffs_data.append({
                        'file_name': file_name_match,
                        'added_lines': [],
                        'deleted_lines': []
                    })

                    current_file = file_name_match
                    # print(file_names)
                continue
            # match line numbers
            if(line.startswith('@@')):
                # match following pattern => @@ -1,21 +0,0
                re_compile = re.compile('@@ -(\d+),?(\d+)? \+(\d+),?(\d+)?')
                matches = re_compile.findall(line)
                # extract types of lines
                from_line = matches[0][0]
                glob_from_line = int(from_line) + 3
                from_count = matches[0][1]
                to_line = matches[0][2]
                to_count = matches[0][3]
                # set count start from diff
                current_line = int(from_line)

                continue

            # check for deleted lines
            if(line.startswith('-') and not line.startswith('---')):
                last_deleted_line += 1
                # if file_name_match in file_names:
                for diffy in diffs_data:
                    if diffy['file_name'] == current_file:
                        # print('incrementing adding' + str(current_line) + "<><> LINE"  + line + "line number " + str(current_line))
                        diffy['deleted_lines'].append(current_line)
                        # print('hit added')
                        # print(current_line)
                    # to be removed
                # else:
                current_line += 1
                continue
                # deleted_lines.append(glob_from_line)
                last_deleted_line += 1
            if(line.startswith('+') and not line.startswith('+++')):
                last_added_line += 1
                # if file_name_match in file_names:
                for diffy in diffs_data:
                    if diffy['file_name'] == current_file:
                        # print("incrementing adding" + str(current_line) + "<><> LINE"  + line + "line number " + str(current_line))
                        diffy['added_lines'].append(current_line)

                current_line += 1
                continue
            if(line.startswith(" ")):
                current_line += 1

            glob_from_line += 1

        return diffs_data
