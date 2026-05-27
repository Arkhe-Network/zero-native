import struct
import hashlib

class ArkheOSGGUF:
    def __init__(self, model_name):
        self.model_name = model_name
        self.metadata = {}
        self.tensors = []

    def set_metadata(self, key, value):
        self.metadata[key] = value

    def add_tensor(self, name, shape, dtype, offset):
        self.tensors.append({
            "name": name,
            "shape": shape,
            "dtype": dtype,
            "offset": offset
        })

    def to_gguf_binary(self):
        # Generate some dummy binary data
        return b"GGUF_MOCK_DATA_" + str(self.metadata).encode() + str(self.tensors).encode()

    def compute_checksum(self):
        return hashlib.sha256(self.to_gguf_binary()).hexdigest()