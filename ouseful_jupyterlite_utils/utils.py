import asyncio
import js

from js import fetch
from pyodide.http import pyfetch

def guess_domain():
    """Guess domain the JupyterLite environment is served from."""
    location = '/'.join(':'.join(str(js.location).split(':')[1:]).split('/')[:-1])
    return location

# Ish via https://til.simonwillison.net/python/sqlite-in-pyodide
from pyodide import open_url

DB_NAME = "JupyterLite Storage"

def remote_load(url):
    """Import and run code from a remote URL."""
    exec(open_url(url).read(), globals())
    
# Via: https://github.com/jupyterlite/jupyterlite/discussions/91#discussioncomment-1137213
async def get_contents(path):
    """Load file from in-browser storage. Contents are in ['content'].
    
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

async def load_file_into_in_mem_filesystem(url, fn=None):
    """Load a file from a URL into an in-memory filesystem."""
     
    # Create a filename if required
    fn = fn if fn is not None else url.split("/")[-1]
     
    # Fetch file from URL
    res = await fetch(url)
     
    # Buffer it
    buffer = await res.arrayBuffer()
     
    # Write file to in-memory file system
    open(fn, "wb").write(bytes(buffer.valueOf().to_py()))
 
    return fn

# There is also another possible implementation
async def load_file_into_in_mem_filesystem2(url, fn=None):
    # Create a filename if required
    fn = fn if fn is not None else url.split("/")[-1]
    res = await pyfetch(url)
    stream = await res.bytes()

    # Write file to in-memory file system
    open(fn, "wb").write(stream)
    
    return fn

# Call as:
# url="https://raw.githubusercontent.com/psychemedia/lang-fairy-books/main/data.db"
# db_file = await load_file_into_in_mem_filesystem(url)

# Demo:
#import sqlite3
# Open database connection
#c = sqlite3.connect(db_file)

# Show database tables
#c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
 