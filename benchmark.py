import os
import time
import requests
import numpy as np
import matplotlib.pyplot as plt
import json

# Replace this with your actual Groq API key
API_KEY = "YOUR_GROQ_API_KEY_HERE"
URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama3-8b-8192",
    "messages": [{"role": "user", "content": "Write a short paragraph about cloud computing."}],
    "stream": True # We stream to measure Time to First Token (TTFT)
}

latencies = []
ttfts = []

print("Starting latency test (20 requests)...")

for i in range(20):
    start_time = time.time()
    response = requests.post(URL, headers=headers, json=payload, stream=True)
    
    ttft = None
    for line in response.iter_lines():
        if line:
            if ttft is None:
                ttft = time.time() - start_time # Time to First Token
            # We just read the stream, we don't need the actual text
            
    end_time = time.time()
    total_time = end_time - start_time
    latencies.append(total_time)
    ttfts.append(ttft)
    
    print(f"Request {i+1}: Total Time = {total_time:.4f}s, TTFT = {ttft:.4f}s")
    time.sleep(0.2) # Small break between requests

# Calculate Percentiles
p50 = np.percentile(latencies, 50)
p95 = np.percentile(latencies, 95)
p99 = np.percentile(latencies, 99)

print("\n--- Results ---")
print(f"Mean Latency: {np.mean(latencies):.4f}s")
print(f"p50 Latency:  {p50:.4f}s")
print(f"p95 Latency:  {p95:.4f}s")
print(f"p99 Latency:  {p99:.4f}s")

# Plotting the CDF (Cumulative Distribution Function)
plt.hist(latencies, bins=10, cumulative=True, density=True, histtype='step', label='Total Latency CDF')
plt.xlabel('Total Latency (s)')
plt.ylabel('Probability')
plt.title('LLM API Latency CDF')
plt.grid(True)
plt.savefig('latency_cdf.png')
print("Saved graph to latency_cdf.png")
