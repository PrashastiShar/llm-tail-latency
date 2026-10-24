# LLM Tail-Latency Benchmark under Network Constraints

This project empirically demonstrates how network jitter affects the tail latency of cloud-based LLM inference APIs, validating the arguments of my independent position paper on edge-cloud LLM evaluation.

## Key Findings
*   **Stable Network:** p50 = 0.24s, p99 = 0.50s
*   **Jittery Network (200ms delay + 50ms jitter):** p50 = 0.89s, p99 = 1.97s
*   **Conclusion:** Average latency metrics mask severe tail-latency degradation. The p95/p99 latency increases by nearly 6x under simulated edge network conditions, making real-time AI applications feel unresponsive.

## Tech Stack
*   Python, Requests (Groq API)
*   Linux `tc netem` (Network Emulator)
*   NumPy, Matplotlib (Data analysis & CDF plotting)

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Add your Groq API key to `benchmark.py`
3. Run baseline: `python3 benchmark.py`
4. Add jitter: `sudo tc qdisc add dev eth0 root netem delay 200ms 50ms`
5. Run jitter test: `python3 benchmark.py`
6. Remove jitter: `sudo tc qdisc del dev eth0 root`
