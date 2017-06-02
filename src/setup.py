from extract import Extract

ext = Extract()
ext.clone_repo("https://github.com/rajikaimal/npm-checker", "/home/rajika/Desktop/test2")
ext.get_parsed_diff("/home/rajika/Desktop/test2")
