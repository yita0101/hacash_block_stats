import time
from block_stats import BlockAnalyzer
import json
import matplotlib.pyplot as plt
from datetime import datetime
import os
import argparse
from x16rs import print_stats

def save_stats_to_file(stats_data, start_height, end_height):
    """Save statistics data to JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stats_{start_height}_to_{end_height}_{timestamp}.json"
    
    # Ensure stats directory exists
    os.makedirs("stats", exist_ok=True)
    
    # Prepare data to save
    data = {
        "start_height": start_height,
        "end_height": end_height,
        "total_blocks": stats_data["total_blocks"],
        "algo_stats": stats_data["algo_stats"],
        "timestamp": timestamp
    }
    
    # Save to JSON file
    with open(f"stats/{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return f"stats/{filename}"

def generate_charts(stats_data, start_height, end_height):
    """Generate statistical charts"""
    algo_names = [
        "BLAKE", "BMW", "GROESTL", "JH", "KECCAK", "SKEIN",
        "LUFFA", "CUBEHASH", "SHAVITE", "SIMD", "ECHO",
        "HAMSI", "FUGUE", "SHABAL", "WHIRLPOOL", "SHA512"
    ]
    
    # Prepare data
    algo_counts = []
    labels = []
    for algo_id, count in stats_data["algo_stats"].items():
        algo_counts.append(count)
        labels.append(algo_names[int(algo_id)])
    
    # Create charts directory
    os.makedirs("charts", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Draw pie chart
    plt.figure(figsize=(12, 8))
    plt.pie(algo_counts, labels=labels, autopct='%1.1f%%')
    plt.title(f'Algorithm Distribution (Block {start_height} to {end_height})')
    pie_filename = f"charts/pie_chart_{start_height}_to_{end_height}_{timestamp}.png"
    plt.savefig(pie_filename)
    plt.close()
    
    # Draw bar chart
    plt.figure(figsize=(15, 8))
    plt.bar(labels, algo_counts)
    plt.xticks(rotation=45)
    plt.title(f'Algorithm Usage Count (Block {start_height} to {end_height})')
    plt.ylabel('Usage Count')
    plt.tight_layout()
    bar_filename = f"charts/bar_chart_{start_height}_to_{end_height}_{timestamp}.png"
    plt.savefig(bar_filename)
    plt.close()
    
    return pie_filename, bar_filename

def main():
    parser = argparse.ArgumentParser(description='Analyze X16RS algorithm distribution in Hacash blocks')
    parser.add_argument('--start', type=int, required=True, help='Starting block height')
    parser.add_argument('--end', type=int, required=True, help='Ending block height')
    args = parser.parse_args()
    
    analyzer = BlockAnalyzer()
    start_height = args.start
    end_height = args.end
    
    print(f"Processing blocks from height {start_height} to {end_height}")
    start_time = time.time()
    
    total_blocks, algo_stats = analyzer.analyze_blocks(start_height, end_height)
    
    # Prepare statistics data
    stats_data = {
        "total_blocks": total_blocks,
        "algo_stats": {str(k): v for k, v in algo_stats.items()}
    }
    
    # Save statistics results
    json_file = save_stats_to_file(stats_data, start_height, end_height)
    print(f"\nStatistics saved to: {json_file}")
    
    # Generate charts
    pie_chart, bar_chart = generate_charts(stats_data, start_height, end_height)
    print(f"Pie chart saved to: {pie_chart}")
    print(f"Bar chart saved to: {bar_chart}")
    
    # Use print_stats from x16rs.py
    counts = [algo_stats.get(i, 0) for i in range(16)]
    total_rounds = sum(counts)
    print_stats(counts, total_rounds)
    
    print(f"\nTotal processing time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main() 