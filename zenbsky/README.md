# **Zen Bluesky: A Random Thought Generator**

Zen Bluesky is a minimalist single-page web application designed to offer a serene, distraction-free reading experience. It fetches a continuous stream of random thoughts and posts from a hand-picked list of public Bluesky profiles, presenting them one at a time. The app is built with a focus on a clean, unobtrusive user interface, allowing for a moment of quiet reflection or discovery without the overwhelming noise of a typical social media feed.

## **Features**

* **Randomized Content Generation:** The application intelligently shuffles a curated list of Bluesky handles to ensure that each new post is selected from a random source. This approach prevents repetitive content and encourages a broader discovery of different voices from the community.  
* **Automated Refresh with a Countdown Timer:** A built-in timer automatically fetches and displays a new post at a fixed interval of 20 seconds. This feature provides a passive, "zen-like" experience where new content simply appears on the screen without any user interaction. The countdown is displayed on the page so users know when the next thought will appear.  
* **Manual Refresh Control:** For moments when a user wants to skip to the next thought, a "Next Thought" button is provided. This gives full control over the pace of consumption, offering a balanced experience between automated and manual interaction.  
* **Aesthetic & Responsive Design:** The app's visual style is inspired by the dark, clean aesthetic of GitHub. It uses a custom CSS theme with variables for a consistent look and smooth CSS transitions and animations to create a polished and engaging user experience. The layout is fully responsive and adjusts gracefully to various screen sizes, from mobile phones to desktop monitors.  
* **Accessibility and SEO-Friendly:** To ensure the page is accessible and easily discoverable, it includes several key features:  
  * **Meta Tags:** Standard SEO meta tags and Open Graph tags are included to improve search engine ranking and enhance how the page is displayed when shared on social media.  
  * **ARIA Attributes:** Important elements like the refresh button and loading indicator have aria-label or aria-live attributes to make the page more navigable for users relying on screen readers.  
* **Robust Error Handling:** The application implements a simple but effective retry mechanism with **exponential backoff**. This means if a fetch request fails (e.g., due to a network issue or an unresponsive handle), the script will automatically retry the request with an increasing delay. This prevents the app from failing completely and improves its resilience to temporary network problems.

## **How It Works**

The core logic of the application is encapsulated in a self-contained JavaScript script. Here's a more detailed breakdown of the process:

1. **Initialization:** When the page loads, a DOMContentLoaded event listener triggers the initial post fetch. The app's state variables and DOM elements are set up.  
2. **Random Handle Selection:** The script first makes a copy of the hardcoded handles array and shuffles it. This randomized list ensures that the application doesn't always start with the same handle, promoting a more diverse feed.  
3. **Data Fetching via a CORS Proxy:** The script attempts to fetch the RSS feed for the first handle in the shuffled list. To bypass Cross-Origin Resource Sharing (CORS) restrictions that would normally block the request, it uses a public CORS proxy (https://corsproxy.io). The RSS feed URL for the selected handle is passed as a parameter to the proxy, which then fetches the data and returns it to the client.  
4. **XML Parsing and Post Extraction:** The fetched data is an XML string. The browser's built-in DOMParser is used to convert this string into a document object model (DOM), allowing the script to query and extract specific pieces of information. It specifically looks for \<item\> tags, which represent individual posts in the feed.  
5. **Content Rendering:** Once a valid post is found, the script extracts the post's text (\<description\>), author details (\<title\> and \<description\> within the \<channel\>), timestamp (\<pubDate\>), and the direct link to the post (\<link\>). It then dynamically creates HTML elements and inserts them into the posts container.  
6. **Animations and Transitions:** The newly created post element is initially hidden. A brief delay of 10 milliseconds is introduced before adding a visible class. This small delay allows the browser to register the element's initial state, enabling the CSS transition to smoothly animate the post's appearance, creating a pleasant "fade and slide in" effect.  
7. **Error and Retry Logic:** If a fetch attempt fails at any stage (e.g., a handle's feed is empty or the network request times out), the script's recursive function will simply move on to the next handle in the shuffled list. If all handles fail, a final error message is displayed, and the retry logic with exponential backoff will be activated to make further attempts.

## **Technologies Used**

* **HTML5:** The foundation of the web page, used for structuring the content with semantic tags like \<main\> and \<article\> to improve readability and accessibility.  
* **CSS3:** Responsible for all the styling, including the color scheme, layout, and visual effects. It uses CSS variables (:root) for easy theme management and transitions for smooth UI feedback.  
* **Vanilla JavaScript:** The application's core logic is written in plain JavaScript without any external libraries or frameworks. This keeps the project lightweight and easy to understand.

## **Usage & Customization**

This project is designed to be a simple, standalone web page. You can run it locally by simply opening the index.html file in your web browser.

To customize the application, you can:

* **Modify the Post Sources:** Edit the handles array in the JavaScript to add, remove, or change the Bluesky profiles you want to pull posts from.
  ```
  const handles \= \[
  'jaygraber.bsky.social',
  'pfrazee.com',
  // ... more handles
  \];
  
* **Adjust the Refresh Interval:** Change the REFRESH\_INTERVAL constant in the JavaScript to set a different time for the automatic refresh.
  ```
  const CONSTANTS \= {
  REFRESH\_INTERVAL: 20, // Time in seconds
  // ... other constants
  };

* **Change the Style:** Update the CSS variables in the \<style\> block to easily change the color palette, fonts, or overall look of the page.
  ```
  :root {
  \--background-color: \#0d1117;
  \--text-color: \#c9d1d9;
  \--secondary-text-color: \#8b949e;
  \--accent-color: \#58a6ff;
  /\* ... more variables \*/
  }
  
## **Contributing**

Contributions are welcome\! If you have suggestions for new features, bug fixes, or new public handles to add to the list, feel free to open a discussion or a pull request.

## **Credits**

* The content is sourced from the Bluesky social network.  
* The CORS proxy used is https://corsproxy.io.

## **License**

This project is open-source and available under the MIT License. You are free to use, modify, and distribute the code for any purpose, as long as you include the original copyright and license notice.

---

> Generated by Google Gemini, refined by Duffin
