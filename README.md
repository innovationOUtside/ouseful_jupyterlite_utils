# ouseful_jupyterlite_utils

Utilities for working with JupyterLite

*This package is intended to provide intermediate support, patches, hacks, fixes and workarounds, as much as anything, for things that you might expect to be able to do, but that aren't yet acheivable, in pyodide and jupyterlite.*

*Please check the source code for attribution of where the various hacks came from... I'll try to add proper attribution notices to this page when I get a chance...*

## Package Features

Package currently includes utilities to load SQLite database into memroy from a URL and tools to load files from URLs and local sreorage into `pandas` dataframes.

### Load SQLite Database into Memory From URL

```python
# Ish via https://til.simonwillison.net/python/sqlite-in-pyodide
from ouseful_jupyterlite_utils.sqlite_utils import load_file_into_in_mem_filesystem

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
df = await pdu.read_csv_url(URL) # Pass separator, if required, as second parameter

A simple, non-await route for loading data into pandas from a URL:

```python
# via @simonw: https://github.com/simonw/datasette-jupyterlite/issues/2#issuecomment-956586201
import pandas, pyodide
pandas.read_csv(pyodide.open_url(URL), sep=";")
# Also available as pdu.read_csv(URL, sep=";")
```

### Load CSV into `pandas` dataframe from local browser storage

```python
#Via @bollwyvl
df = await pdu.read_csv_local("iris.csv")
df
```

## Installation

This package is intended to be used with JupyterLite in a pyodide kernel.

It can be installed using micropip from the wheel in this repo:

```python
import micropip

package_url = "https://raw.githubusercontent.com/innovationOUtside/ouseful_jupyterlite_utils/main/ouseful_jupyterlite_utils-0.0.2-py3-none-any.whl"

await micropip.install(package_url)
#await micropip.install("pandas")
```

To build the wheel from the package source: `pip wheel .`

TO DO: automation to build the wheel and update the README to use new version wheels.
