from js import fetch
# Ish via https://til.simonwillison.net/python/sqlite-in-pyodide

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

# Call as:
# url="https://raw.githubusercontent.com/psychemedia/lang-fairy-books/main/data.db"
# db_file = await load_file_into_in_mem_filesystem(url)

# Demo:
#import sqlite3
# Open database connection
#c = sqlite3.connect(db_file)

# Show database tables
#c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
 