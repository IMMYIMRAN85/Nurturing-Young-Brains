console.log("Content script is running on YouTube...");

const getVideoTitle = () => {
  const titleElement = document.querySelector('yt-formatted-string.style-scope.ytd-watch-metadata');

  if (titleElement) {
    console.log("Video Title:", titleElement.innerText);
  } else {
    console.log("Video title not found!");
  }
};

// Wait 2 seconds before running
setTimeout(getVideoTitle, 2000);