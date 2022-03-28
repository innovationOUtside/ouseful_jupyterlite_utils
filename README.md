# ouseful_jupyterlite_utils

Utilities for working with JupyterLite

*This package is intended to provide intermediate support, patches, hacks, fixes and workarounds, as much as anything, for things that you might expect to be able to do, but that aren't yet acheivable, in pyodide and jupyterlite.*

*Please check the source code for attribution of where the various hacks came from... I'll try to add proper attribution notices to this page when I get a chance...*


## Handy Tricks

A collection of handy tricks, collected from various source, some of which are bundled inside the package created from this repo.

### What platform am I on?

Check what platform you are on. For example:

```python
import platform as p

p.platform(), p.system(), p.machine(), p.architecture()
"""
('Emscripten-1.0-wasm32-32bit', 'Emscripten', 'wasm32', ('32bit', ''))
"""
```

### What domain am I on?

Guess at the domain the environment is being served from:

```python

import js
from pathlib import Path

def guess_domain():
    """Guess domain the JupyterLite environment is served from."""
    location = '/'.join(':'.join(str(js.location).split(':')[1:]).split('/')[:-1])
    return location

guess_domain()

"""
'http://localhost:9000'
"""
```

### How do I reset a modified, distributed file back to the original?

If a file is shipped with the JupyterLite distribution, you can open it, edit it, and save the modified version to browser storage. To reet the file to the original, shipped version, just delete it... This will delete it from the browser storage and it will reappear in its original form. (If for some reason it doesn't reappear after deleting it, just reload the JupyterLite enviroment.)

### How do I use `requests`'?

The `requests` package doesn't work out of the can, but here's a way round it for now... [*Making the Python requests module work in Pyodide*](https://bartbroere.eu/2021/11/05/pyodide-requests/) and [`bartbroere/pyodide-requests`](https://github.com/bartbroere/pyodide-requests).

### Load in file from remote URL

We can easily read in a file from a remote URL using `pyodide.open_url(url)`:

```python
from pyodide import open_url

url="https://raw.githubusercontent.com/innovationOUtside/ouseful_jupyterlite_utils/main/ouseful_jupyterlite_utils/utils.py"

open_url(url).read()
```

## Installation

This package is intended to be used with JupyterLite in a pyodide kernel.

It can be installed using micropip from the wheel in this repo:

```python
import micropip

package_url = "https://raw.githubusercontent.com/innovationOUtside/ouseful_jupyterlite_utils/main/ouseful_jupyterlite_utils-0.0.4-py3-none-any.whl"

await micropip.install(package_url)
```

To build the wheel from the package source: `pip3 wheel .`

TO DO: automation to build the wheel and update the README to use new version wheels.

## Package Features

Package currently includes utilities to load remote files into memory (for example, load a remote SQLite database into memory from a URL) and tools to load files from URLs and local sreorage into `pandas` dataframes.

## Load function in from remote URL

We can load a code file in from a remote URL and then `exec()` it to run the code in the file (via @dougRzz):

```python
import pyodide

# Load in the contents of `ouseful_jupyterlite_utils/utils` package from a remote URL:

URL = "https://raw.githubusercontent.com/innovationOUtside/ouseful_jupyterlite_utils/main/ouseful_jupyterlite_utils/utils.py"
exec(pyodide.open_url(URL).read())

# The `get_content()` function inside that file will now be available to call.
# Note that if the file tries to load in local relative files imported inside the package, they won't be available
```

The trick is also packaged as follows:

```python
from ouseful_jupyterlite_utils.utils import remote_load

remote_load??
```

## Load Text file from local browser storage

We can load the contents of a file in from local browser storage

```python
from ouseful_jupyterlite_utils.utils import get_contents

f = await get_contents("test.md")
f
"""
{'name': 'test.md',
 'path': 'test.md',
 'last_modified': '2022-03-14T17:29:45.657Z',
 'created': '2022-03-14T17:28:45.142Z',
 'format': 'text',
 'mimetype': 'text/plain',
 'content': '# Heading\n\nExample text.\n',
 'size': None,
 'writable': True,
 'type': 'file'}
"""

# Contents are in: f['content']
# Also access file contents eg via `import io ; io.StringIO(f["content"])`
```

### Getting a File into Local Browser Storage

Just because you can see a file in the JupyterLab file browser doesnlt mean it's in browser storage. If you use browser developer tools, you can look to see what *is* available there.

![image](https://user-images.githubusercontent.com/82988/160463048-55a6abf8-1c00-4fd4-b03a-757469c02424.png)

To ensure that e.g. a data file *is* available in browser storage, you can double click on it in the file browser to open it __and then save it__. This will have the side effect of saving it into browser storage.


### Load SQLite Database into Memory From URL

```python
# Ish via https://til.simonwillison.net/python/sqlite-in-pyodide
from ouseful_jupyterlite_utils.utils import load_file_into_in_mem_filesystem

# Call as:
url="https://raw.githubusercontent.com/psychemedia/lang-fairy-books/main/data.db"
db_file = await load_file_into_in_mem_filesystem(url)
# Use: fn="mydb.db" to specify db name
# Otherwise, the file is saved using the original file name

# Demo:
import sqlite3
# Open database connection
c = sqlite3.connect(db_file)

# Show database tables
c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
```

### Load CSV File From a URL into a `pandas` Dataframe

```python
from ouseful_jupyterlite_utils import pandas_utils as pdu

# Load CSV from URL
# Via @jtpio
URL = "https://support.staffbase.com/hc/en-us/article_attachments/360009197031/username.csv"
df = await pdu.read_csv_url(URL, sep=";") # Pass separator, if required, as second parameter
```

A simple, non-await route for loading data into pandas from a URL:

```python
# via @simonw: https://github.com/simonw/datasette-jupyterlite/issues/2#issuecomment-956586201
import pandas, pyodide
pandas.read_csv(pyodide.open_url(URL), sep=";")
# Also available as pdu.read_csv(URL, sep=";")
```

### Load pickle file from URL

Ish [via @rth](https://github.com/jupyterlite/jupyterlite/issues/119#issuecomment-1025817324):

```python
import pickle
from ouseful_jupyterlite_utils.utils import get_stream_from_url

url = "https://raw.githubusercontent.com/jmshea/digicom-jupyter/main/content/signals.pkl"

stream = await get_stream_from_url(url)
data = pickle.loads(stream)
data
```

### Load CSV into `pandas` dataframe from local browser storage

```python
#Via @bollwyvl
df = await pdu.read_csv_local("iris.csv") # Use default separator
df
```
