import os
import re


class Parse:

    def read_file(self, file_name):
        full_path = os.path.dirname(
            os.path.realpath(__file__)) + file_name
        with open(full_path, "r") as content:
            content_str = content.read()
        print(content_str)
        return [content_str]

    # test with local file -> todo convert to fetch from HTTP
    def parse_diff_file(self, file_name):
        diff = self.read_file(file_name)
        if(diff == ""):
            return False
        else:
            parsed_diff = diff[0].split('\n')
            self.parse_diff_github(parsed_diff)
            return parsed_diff

    def parse_diff_github(self, lines):
        deleted_lines = []
        for line in lines:
            matched_line = line.startswith("diff --git")
            print(matched_line)

    def parse_blame(self, blame):
        return "Parsing blame"
