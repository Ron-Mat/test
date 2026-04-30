# Sample data: A list of candidates
candidates = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
]

# Practice Task: Find the average score
total_score = sum(c["score"] for c in candidates)
average = total_score / len(candidates)

print(f"Candidate Data: {candidates}")
print(f"Average Score: {average}")
# TODO@Ron-Mat #1 