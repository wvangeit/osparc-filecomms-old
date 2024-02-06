oSparc File Communications Python Library
=========================================

This library is meant to perform stable file-based communications between python code that runs in oSparc services.

Installation
------------
```
pip install osparc-filecomms
```

Handshake Usage
---------------

With a handshake two services can exchange each other's ID, with a guarantee that the service on the other side is alive.
The protocol has an 'initiator' and a 'receiver'.

```
from osparc-filecomms import handshakers
import uuid

# Existing input/output directories
input_dir = Path("input_dir") 
output_dir = Path("output_dir")

my_uuid = str(uuid.uuid4())

handshaker = handshakers.FileHandshaker(my_uuid, input_dir, output_dir, is_initiator=True)

other_side_uuid = handshaker.shake()
print(f"I performed a handshake. My uuid is: {my_uuid}. The other side's uuid is: {other_side_uuid}")
```

After this code has run on both sides, both uuid's can be used in data files that are exchanged. 
If the processes accessing these files make sure the receiver and sender uuid match, they can be sure the files are coming from another service that is live.
