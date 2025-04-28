import json

# List of simple bad words (you can expand this later)
bad_words = ["bad", "stupid", "hate", "violence", "idiot", "kill", "hurt"]

# Path to the comments.json file
COMMENTS_FILE = 'backend/model/comments.json'

# Function to load comments
def load_comments():
    try:
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['comments']
    except Exception as e:
        print("Error loading comments:", e)
        return []

# Function to check for bad words
def check_comments(comments):
    for idx, comment in enumerate(comments, start=1):
        comment_lower = comment.lower()
        found_bad_words = [word for word in bad_words if word in comment_lower]
        
        if found_bad_words:
            print(f"[DANGEROUS] Comment {idx}: {comment}")
            print(f"    🔥 Bad words detected: {found_bad_words}")
        else:
            print(f"[SAFE] Comment {idx}: {comment}")

# Main logic
if __name__ == "__main__":
    comments = load_comments()
    if comments:
        check_comments(comments)
    else:
        print("No comments found or failed to load!")
