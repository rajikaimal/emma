# emma

> WIP !!!

## Developement setup

### Setup ngrok

Download and install [ngrok](https://ngrok.com/download) 

Run ngrok

```
$ ./ngork http [port]
```

### Setup GitHub webhook

> TODO

Run emma

```
$ bash ./init.sh
```

## Enpoints

#### /payload

## Programatic API

```py
from emma import Parser

# create parser object
parser = Parser()

# parse local diff file - returns a generator
parsed_diff = parser.parse_diff('/home/rajika/projects/sublime-vmd', 'master')

# parse raw diff to get following dict
#  {
#      'file_names': file_names,
#      'deleted_lines': deleted_lines,
#      'added_lines': added_lines
#  }

parsed_raw_diff = parser.parse_raw_diff(raw_diff)

```

## Algorithm

> TODO ...

### Data set generation

### Heuristics
