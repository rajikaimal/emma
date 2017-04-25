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
            # print(commit)
            raw_diff = r_git.diff(temp_commit['commit'], commit)
            parsed_diff = self.parse_raw_diff(raw_diff)
            # print('Parsed diff ' + str(parsed_diff))
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
                    'file_names': parsed_diff['file_names'],
                    'added_lines': parsed_diff['added_lines'],
                    'deleted_lines': parsed_diff['deleted_lines'],
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
        file_names = []
        deleted_lines = []
        added_lines = []
        last_deleted_line = 0
        last_added_line = 0
        current_line = 0
        
        glob_from_line = 0
        new_file = False

        for line in raw_diff_lines:
            
            if(line.startswith('diff --git')):
                is_diff = False
                # last_deleted_line = 0
                glob_from_line = 0
                last_added_line = 0
                current_line = 0
                glob_from_line = 0

            # match line changes --- && +++
            # if(line.startswith('--- ')):
            #     is_diff = True
            # elif(line.startswith('+++ ')):
            #     is_diff = True
            # else:
            #     is_diff = False

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
                current_line += 1
                continue
                # check for deleted lines
            if(line.startswith('---') or line.startswith('+++')):
                current_line += 1
                re_compile = re.compile('--- a/(\w+)')
                matches = re_compile.findall(line)
                for file_name_match in matches:
                    file_names.append(file_name_match)
                continue
            if(line.startswith('-')):
                last_deleted_line += 1
                deleted_lines.append(glob_from_line)
                last_deleted_line += 1
            if(line.startswith('+')):
                last_added_line += 1
                # added_lines.append({
                #     'from': glob_from_line,
                #     'no': last_added_line
                # })
                added_lines.append(glob_from_line)

            current_line += 1
            glob_from_line += 1
                
        return {
            'file_names': file_names,
            'deleted_lines': deleted_lines,
            'added_lines': added_lines
        }

parser = Parser()
