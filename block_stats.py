import requests
import json
from x16rs import X16RS
import binascii
import struct
import time
from collections import defaultdict

class BlockAnalyzer:
    def __init__(self, node_url="http://127.0.0.1:8081"):
        self.node_url = node_url
        self.x16rs = X16RS()
        
    def get_block_data(self, height):
        """Get block data at specified height"""
        url = f"{self.node_url}/query/block/intro"
        params = {"height": height}
        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            print(f"Failed to get block {height} data: {str(e)}")
            return None

    def construct_block_data(self, block):
        data = bytearray()
        
        # version (2 bytes) - little endian
        data.extend(struct.pack("<H",block["version"]))  # generates 01 00
        
        # height (4 bytes) - big endian
        data.extend(struct.pack(">I", block['height']))
        
        # 00 (1 byte)
        data.extend(b'\x00')
        
        # timestamp (4 bytes) - big endian
        data.extend(struct.pack(">I", block['timestamp']))
        
        # prevhash (32 bytes)
        prev_hash = bytes.fromhex(block['prevhash'])
        data.extend(prev_hash)
        
        # mrklroot (32 bytes)
        merkle_root = bytes.fromhex(block['mrklroot'])
        data.extend(merkle_root)
        
        # transaction count (4 bytes) - big endian, need to add 1
        data.extend(struct.pack(">I", block['transaction'] + 1))
        
        # nonce (4 bytes) - big endian
        data.extend(struct.pack(">I", block['nonce']))
        
        # difficulty (4 bytes) - big endian
        data.extend(struct.pack(">I", block['difficulty']))
        
        # 0000 (2 bytes)
        data.extend(b'\x00\x00')
        
        # Verify data length (should be 89 bytes)
        expected_length = 2 + 4 + 1 + 4 + 32 + 32 + 4 + 4 + 4 + 2  # = 87 bytes
        if len(data) != expected_length:
            raise ValueError(f"Constructed data length error: expected {expected_length} bytes, got {len(data)} bytes")

        # Debug information
        # print(f"Constructed data (hex): {data.hex()}")
        
        # Print field values for debugging
        # print(f"Version: {data[0:2].hex()}")
        # print(f"Height: {data[2:6].hex()}")
        # print(f"Separator: {data[6:7].hex()}")
        # print(f"Timestamp: {data[7:11].hex()}")
        # print(f"PrevHash: {data[11:43].hex()}")
        # print(f"MerkleRoot: {data[43:75].hex()}")
        # print(f"TxCount: {data[75:79].hex()}")
        # print(f"Nonce: {data[79:83].hex()}")
        # print(f"Difficulty: {data[83:87].hex()}")
        
        return data

    def analyze_blocks(self, start_height, end_height):
        """Analyze blocks in specified range"""
        total_blocks = 0
        algo_stats = defaultdict(int)
        
        for height in range(start_height, end_height + 1):
            if height % 200 == 0:
                print(f"Processing block {height}...")
                
            block = self.get_block_data(height)
            if not block:
                continue
                
            # Construct block data
            block_data = self.construct_block_data(block)
            
            # First calculate SHA3-256 hash
            from hashlib import sha3_256
            sha3_input = sha3_256(block_data).digest()
            # print(f"SHA3-256 result: {sha3_input.hex()}")
            
            # Calculate repeat count
            repeat = height // 50000 + 1
            if repeat > 16:
                repeat = 16
                
            # Calculate X16RS hash using SHA3 result
            try:
                hash_result, counts = self.x16rs.hash(repeat, sha3_input)
                # print(f"X16RS result: {hash_result.hex()}")
                
                # Count algorithm usage
                for algo, count in enumerate(counts):
                    algo_stats[algo] += count
                    
                total_blocks += 1
                
            except Exception as e:
                print(f"Error processing block {height}: {str(e)}")
                
        return total_blocks, algo_stats

def main():
    analyzer = BlockAnalyzer()
    start_height = 591819
    end_height = 591819
    
    print(f"Starting analysis for blocks {start_height} to {end_height}")
    start_time = time.time()
    
    total_blocks, algo_stats = analyzer.analyze_blocks(start_height, end_height)
    
    # Print statistics
    algo_names = [
        "BLAKE", "BMW", "GROESTL", "JH", "KECCAK", "SKEIN",
        "LUFFA", "CUBEHASH", "SHAVITE", "SIMD", "ECHO",
        "HAMSI", "FUGUE", "SHABAL", "WHIRLPOOL", "SHA512"
    ]
    
    print("\nStatistics Results:")
    print(f"Total blocks: {total_blocks}")
    print("\nAlgorithm Usage Statistics:")
    
    total_rounds = sum(algo_stats.values())
    for algo_id, count in algo_stats.items():
        percentage = (count * 100.0) / total_rounds
        print(f"{algo_names[algo_id]}: {count} times ({percentage:.2f}%)")
        
    print(f"\nTotal time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main() 