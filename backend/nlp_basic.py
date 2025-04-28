import json
import re  # Regular Expressions module for smarter matching
import datetime  # For timestamps in the summary log

# List of simple bad words (expand as needed)
bad_words = ["bad", "stupid", "hate", "violence", "idiot", "kill", "hurt"]

# Paths
COMMENTS_FILE = 'backend/model/comments.json'
DANGEROUS_FILE = 'backend/model/dangerous_comments.json'
SUMMARY_FILE = 'backend/model/summary.txt'
FULL_LOG_FILE = 'backend/model/full_comments_log.json'  # <-- New full log file

# Function to load comments
def load_comments():
    try:
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['comments']
    except Exception as e:
        print("Error loading comments:", e)
        return []

# Function to save full log (safe and dangerous)
def save_full_log(all_comments_log):
    try:
        with open(FULL_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"log": all_comments_log}, f, ensure_ascii=False, indent=4)
        print(f"\n📚 Full comments log saved to '{FULL_LOG_FILE}'.")
    except Exception as e:
        print("Error saving full comments log:", e)

# Function to append the summary of each run
def save_summary(dangerous_count):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(SUMMARY_FILE, 'a', encoding='utf-8') as f:  # 'a' = append mode
            f.write("\n--------------------------------------\n")
            f.write(f"Summary (Generated on {now})\n")
            if dangerous_count > 0:
                f.write(f"⚠️ {dangerous_count} dangerous comments detected and saved.\n")
            else:
                f.write("✅ No dangerous comments detected. Nothing to save.\n")
            f.write("--------------------------------------\n")
        print(f"\n📝 Summary appended to '{SUMMARY_FILE}'.")
    except Exception as e:
        print("Error saving summary:", e)

# Function to check comments
def check_comments(comments):
    dangerous_comments = []   # Dangerous comments only
    all_comments_log = []     # Full log of every comment

    for idx, comment in enumerate(comments, start=1):
        comment_lower = comment.lower()
        found_bad_words = []

        for word in bad_words:
            # Match full words only
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, comment_lower):
                found_bad_words.append(word)

        if found_bad_words:
            print(f"[DANGEROUS] Comment {idx}: {comment}")
            print(f"    🔥 Bad words detected: {found_bad_words}")
            dangerous_comments.append({
                "comment": comment,
                "bad_words_detected": found_bad_words
            })
            all_comments_log.append({
                "comment": comment,
                "status": "DANGEROUS",
                "bad_words_detected": found_bad_words
            })
        else:
            print(f"[SAFE] Comment {idx}: {comment}")
            all_comments_log.append({
                "comment": comment,
                "status": "SAFE",
                "bad_words_detected": []
            })

    # Save dangerous comments to JSON if any
    if dangerous_comments:
        try:
            with open(DANGEROUS_FILE, 'w', encoding='utf-8') as f:
                json.dump({"dangerous_comments": dangerous_comments}, f, ensure_ascii=False, indent=4)
            print(f"\n⚠️ Saved {len(dangerous_comments)} dangerous comments to '{DANGEROUS_FILE}'.")
        except Exception as e:
            print("Error saving dangerous comments:", e)

    # Save full log
    save_full_log(all_comments_log)

    # Save run summary
    save_summary(len(dangerous_comments))

# Main script execution
if __name__ == "__main__":
    comments = load_comments()
    if comments:
        check_comments(comments)
    else:
        print("No comments found or failed to load!")