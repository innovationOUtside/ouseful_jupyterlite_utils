import asyncio
import js

DB_NAME = "JupyterLite Storage"

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
