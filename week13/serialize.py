from random import randint
import json
import pickle
import marshal
import uuid
import sys


print("Comparing the size ...")
print(f"{'JSON':8}{'Pickle':8}{'Marshal':8}")

for i in range(10):
    data = [str(uuid.uuid4()) for i in range(randint(1, 100))]
    json_size = sys.getsizeof(json.dumps(data))
    pickle_size = sys.getsizeof(pickle.dumps(data))
    marshal_size = sys.getsizeof(marshal.dumps(data))
    print(f"{json_size:<8}{pickle_size:<8}{marshal_size:<8}")
