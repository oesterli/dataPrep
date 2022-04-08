## GENERATING UUIDs

import uuid

for i in range(10):
    uuidList = uuid.uuid4(i)                           # creates uuid for each object
print(uuidList)
