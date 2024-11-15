# Hacash X16RS Algorithm Distribution Analyzer

This tool analyzes the distribution of different hashing algorithms in Hacash's X16RS mining algorithm across specified block ranges.

## Prerequisites

- Python 3.7 or higher
- A running Hacash full node
- Required Python packages: matplotlib, requests

## Installation

1. Clone this repository
2. Install required packages:
   pip install matplotlib requests

## Usage

1. Ensure your Hacash full node is running and fully synced
2. Run the analysis script:
   python run_stats.py --start START_BLOCK --end END_BLOCK

Example:
   python run_stats.py --start 500000 --end 500100

## Output

The script generates:
1. JSON statistics file in the 'stats' directory
2. Pie chart visualization in the 'charts' directory
3. Bar chart visualization in the 'charts' directory
4. Console output with detailed statistics

## Statistics Information

The tool analyzes the distribution of these 16 hashing algorithms:
- BLAKE
- BMW
- GROESTL
- JH
- KECCAK
- SKEIN
- LUFFA
- CUBEHASH
- SHAVITE
- SIMD
- ECHO
- HAMSI
- FUGUE
- SHABAL
- WHIRLPOOL
- SHA512


