# ouseful_jupyterlite_utils

Utilities for working with JupyterLite

Package currently includes:

```python
from ouseful_jupyterlite_utils import pandas_utils as pdu

# Load CSV from URL
URL = "https://support.staffbase.com/hc/en-us/article_attachments/360009197031/username.csv"
df = await read_csv_url(URL, "\t")

# Load CSV from local browser storage
df = await read_csv_jupyterlite("iris.csv", "\t")
df
```

## Installation

This package is intended to be used with JupyterLite in a pyodide kernel.

It can be installed using micropip from the wheel in this repo:

```python
import micropip

package_url = "https://raw.githubusercontent.com/innovationOUtside/ouseful_jupyterlite_utils/main/src/ouseful_jupyterlite_utils-0.0.1-py3-none-any.whl"

await micropip.install(package_url)
```

To build the wheel from the package source: `pip wheel .`

TO DO: automation to build the wheel and update the README to use new version wheels.