import ctypes
from pathlib import Path
import platform
import os

class X16RS:
    def __init__(self):
        # Dynamically detect library path
        lib_path = "./lib/libx16rs.dll"
        try:
            self.lib = ctypes.CDLL(lib_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load library: {e}\nPath: {lib_path}")
        
        # Set function parameter types
        self.lib.x16rs_hash.argtypes = [
            ctypes.c_int,                    # loopnum
            ctypes.POINTER(ctypes.c_char),   # input_hash
            ctypes.POINTER(ctypes.c_char),   # output_hash
            ctypes.POINTER(ctypes.c_int)     # counts
        ]
        self.lib.x16rs_hash.restype = None

    @staticmethod
    def get_hash_repeat(block_height):
        """Calculate hash iterations based on block height"""
        repeat = block_height // 50000 + 1
        return min(repeat, 16)

    def hash(self, loop_num, input_data):
        """
        Calculate x16rs hash
        :param loop_num: Number of iterations
        :param input_data: Input data (32 bytes)
        :return: (hash_result, algo_counts)
        """
        if len(input_data) != 32:
            raise ValueError("Input must be 32 bytes")

        # Prepare input buffer
        input_buffer = (ctypes.c_char * 32).from_buffer_copy(input_data)
        
        # Prepare output buffer
        output_buffer = (ctypes.c_char * 32)()
        
        # Prepare count array
        counts = (ctypes.c_int * 16)()

        try:
            # Call C function
            self.lib.x16rs_hash(loop_num, input_buffer, output_buffer, counts)
        except Exception as e:
            raise RuntimeError(f"Error calling x16rs_hash: {e}")

        # Convert results
        hash_result = bytes(output_buffer)
        algo_counts = list(counts)

        return hash_result, algo_counts


def print_stats(counts, total_rounds):
    """Print algorithm statistics"""
    algo_names = [
        "BLAKE", "BMW", "GROESTL", "JH", "KECCAK", "SKEIN",
        "LUFFA", "CUBEHASH", "SHAVITE", "SIMD", "ECHO",
        "HAMSI", "FUGUE", "SHABAL", "WHIRLPOOL", "SHA512"
    ]
    
    print("\nHash Function Statistics:")
    print(f"Total rounds: {total_rounds}")
    print("Algorithm execution counts:")
    
    for i, count in enumerate(counts):
        if count > 0:
            percentage = (count * 100.0) / total_rounds
            print(f"{algo_names[i]}: {count} times ({percentage:.1f}%)")