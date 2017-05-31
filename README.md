# emma

> WIP !!!

:santa: Intelligent mention bot for GitHub organizations

## Install

```
$ pip3 install -r requirements.txt
```

## Deploy

```
$ sh deploy.sh [provider]
```

## Developement setup

### Setup ngrok

Download and install [ngrok](https://ngrok.com/download) 

Run ngrok

```
$ ./ngork http [port]
```

### Setup GitHub webhook

Goto Repository -> `Settings` -> `Webhooks` -> `Add webhook`

Add `Payload URL` from `ngrok` public URL. Click on `Add webhook`

### Add configuration file

```
[Credentials]
username = *********
password = *********

[Repository]
org = *********
repo = *********
```

Run emma

```
$ bash ./init.sh
```

## Enpoints

#### /payload

## Programmatic API

```py
from emma import Parser

# create parser object
parser = Parser()

# parse local diff file - returns a generator
parsed_diff = parser.parse_diff('/home/rajika/projects/sublime-vmd', 'master')
print(parsed_diff)

# parse raw diff to get following dict
#  {
#      'file_names': file_names,
#      'deleted_lines': deleted_lines,
#      'added_lines': added_lines
#  }

parsed_raw_diff = parser.parse_raw_diff(raw_diff)

```

```py
from emma import Parser

# create parser object
parser = Parser()

# parse diff from GitHub diff
parsed_diff = parser.get_pr_diff('https://patch-diff.githubusercontent.com/raw/facebook/react/pull/3.diff')
print(parsed_diff)

```

## Algorithm

`Emma` uses `supervised learning` in machine learning to learn about a given repository. With the increase of data set, emma becomes more intelligent. Therefore mature repositories can gain better results.

### Dataset generation

`Emma` generates a data set for each and every repo in order to train the machine learning model. Dataset is structured as follows.

- Filename, Timestamp, Commit author, Previous author

eg - `bin,321,2017-04-18T19:47:30+0518,inbox.rajika@gmail.com,inbox.rajika@gmail.com`

### Heuristics

Following are the heuristics used by `emma` to predict the best possible reviewer for a pull request.
- Deleted lines
- Added lines
- Modified lines
