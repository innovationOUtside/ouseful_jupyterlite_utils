import pandas as pd
import asyncio, js, io, pandas, IPython
from js import fetch

import warnings 
warnings.filterwarnings("ignore")

DB_NAME = "JupyterLite Storage"

# Via: https://github.com/jupyterlite/jupyterlite/discussions/91#discussioncomment-1137213
async def get_contents(path):
    """Load CSV file from in-browser storage into pandas dataframe.
    
    Use the IndexedDB API to access JupyterLite's in-browser (for now) storage
    
    For documentation purposes, the full names of the JS API objects are used.
    
    See https://developer.mozilla.org/en-US/docs/Web/API/IDBRequest
    """
    # we only ever expect one result, either an error _or_ success
    queue = asyncio.Queue(1)
    
    IDBOpenDBRequest = js.self.indexedDB.open(DB_NAME)
    IDBOpenDBRequest.onsuccess = IDBOpenDBRequest.onerror = queue.put_nowait
    
    await queue.get()
    
    if IDBOpenDBRequest.result is None:
        return None
        
    IDBTransaction = IDBOpenDBRequest.result.transaction("files", "readonly")
    IDBObjectStore = IDBTransaction.objectStore("files")
    IDBRequest = IDBObjectStore.get(path, "key")
    IDBRequest.onsuccess = IDBRequest.onerror = queue.put_nowait
    
    await queue.get()
    
    return IDBRequest.result.to_py() if IDBRequest.result else None

# Via: https://github.com/jupyterlite/jupyterlite/issues/119#issuecomment-854495013
async def read_csv_local(fn, sep=","):
    """"""
    return pd.read_csv(io.StringIO((await get_contents(fn))["content"]), sep = sep)

#df = await read_csv_jupyterlite("iris.csv", "\t")
#df

async def read_csv_url(url, sep=",", dummy_fn="_data.csv"):
    """Load CSV file from URL into pandas dataframe."""
    res = await fetch(url)
    text = await res.text()


    with open(dummy_fn, 'w') as f:
        f.write(text)

    data = pd.read_csv(dummy_fn, sep=sep)
    return data

#URL = "https://support.staffbase.com/hc/en-us/article_attachments/360009197031/username.csv"
#df = await read_csv_url(URL, "\t")
#df