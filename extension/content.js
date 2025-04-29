console.log("🚀 Content script is running on YouTube...");

// --- Grab Video Title ---
const getVideoTitle = () => {
  const titleElement = document.querySelector('yt-formatted-string.style-scope.ytd-watch-metadata');
  if (titleElement) {
    return titleElement.innerText.trim();
  } else {
    console.log("⚠️ Video title not found!");
    return "Unknown Title";
  }
};

// --- Auto Scroll Function ---
const autoScroll = (times, interval, callback) => {
  let count = 0;
  const scrolling = setInterval(() => {
    window.scrollBy(0, 500); // Scroll down by 500 pixels
    count++;
    if (count >= times) {
      clearInterval(scrolling);
      console.log("✅ Auto-scrolling finished!");
      callback();
    }
  }, interval);
};

// --- Grab YouTube Comments ---
const getComments = () => {
  const commentElements = document.querySelectorAll('ytd-comment-thread-renderer #content-text');
  const maxComments = 10; // How many comments to send
  let commentsArray = [];

  if (commentElements.length > 0) {
    console.log(`✅ Found ${commentElements.length} comments. Preparing first ${maxComments} to send.`);
    commentElements.forEach((comment, index) => {
      if (index < maxComments) {
        commentsArray.push(comment.innerText.trim());
      }
    });

    // Send the title + comments to the backend
    sendDataToBackend(getVideoTitle(), commentsArray);

  } else {
    console.log("❌ No comments found!");
  }
};

// --- Send Data to Backend ---
const sendDataToBackend = (videoTitle, commentsArray) => {
  fetch('http://127.0.0.1:5000/upload', { // ✅ FIXED: correct Flask endpoint
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      video_title: videoTitle,
      comments: commentsArray
    })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not OK');
    }
    return response.json();
  })
  .then(data => {
    console.log("✅ Server response:", data);
  })
  .catch(error => {
    console.error("❌ Error sending data to backend:", error);
  });
};

// --- Start Auto Scroll then Get Comments ---
setTimeout(() => {
  console.log("🚀 Starting auto-scroll and comment extraction...");
  autoScroll(15, 800, getComments);  
  // Scroll 15 times, every 800ms, then grab and send comments
}, 4000);
