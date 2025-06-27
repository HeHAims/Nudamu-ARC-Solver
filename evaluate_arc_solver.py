import json
import os

BENCHMARK_FILE = "benchmark_results.json"

if not os.path.exists(BENCHMARK_FILE):
    print(f"❌ File '{BENCHMARK_FILE}' not found. Run nudamu_controller.py first.")
    exit(1)

with open(BENCHMARK_FILE, "r") as f:
    results = json.load(f)

if not results:
    print("❌ No benchmark results found.")
    exit(1)

total = len(results)
success = sum(1 for r in results if r.get("score", 0) >= 1.0)
partial = sum(1 for r in results if 0 < r.get("score", 0) < 1.0)
failure = sum(1 for r in results if r.get("score", 0) == 0)
avg_score = sum(r.get("score", 0) for r in results) / total

print("\n📊 Nudamu ARC Evaluation Results")
print("-------------------------------")
print(f"✅ Perfectly solved: {success} / {total}")
print(f"🟡 Partial scores: {partial}")
print(f"❌ Failed: {failure}")
print(f"📈 Estimated ARC Score: {avg_score:.4f}")
