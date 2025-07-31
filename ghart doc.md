# **GitHub Contributions Art Documentation**

This document provides an overview and usage instructions for the "GitHub Contributions Art" web page, which allows users to visualize GitHub contribution graphs.

## **Purpose**

The primary purpose of this tool is to provide a simple and aesthetically pleasing way to view GitHub contribution graphs for any public GitHub user. It leverages an external service to generate the graph images, focusing on the visual patterns created by development activity.

## **Features**

* **GitHub-Inspired Design:** A dark-themed user interface that mimics the look and feel of GitHub.  
* **Dark/Light Mode Toggle:** A button to switch between a dark theme (default) and a light theme, with the user's preference saved in local storage for future visits.  
* **Dynamic Graph Display:**  
  * Enter a GitHub username to fetch and display their contribution graph.  
  * A loading spinner indicates when the graph is being fetched.  
  * Clear error messages for invalid usernames, network issues, or excluded users.  
* **Image Saving:** Users can download the displayed contribution graph as an SVG image.  
* **Keyboard Interaction:** Pressing the "Enter" key in the username input field triggers the graph display.  
* **Privacy Controls:** An internal list of excluded usernames prevents specific graphs from being displayed for privacy reasons.  
* **Informative Text:** Includes a brief explanation of the tool's creation and a note about its privacy features.

## **Usage**

1. **Open the Web Page:** Open the ghart.html file in your web browser.  
2. **Enter Username:** In the input field labeled "Enter GitHub username," type the GitHub username of the person whose contribution graph you wish to view.  
3. **View Graph:**  
   * Click the "View Graph" button, OR  
   * Press the Enter key on your keyboard while the input field is focused.  
4. **Graph Display:** The contribution graph will appear in the designated area. If there's a problem (e.g., invalid username, network issue, or the username is excluded), an appropriate error message will be displayed.  
5. **Save Image (Optional):** Once the graph is displayed, a "Save Image" button will appear. Click this button to download the contribution graph as an SVG file to your device.  
6. **Toggle Theme (Optional):** Click the sun/moon icon button in the top-right corner to switch between dark and light modes. Your preference will be saved for your next visit.

## **Technical Details**

The web page is built using standard web technologies:

* **HTML5:** Provides the basic structure and content of the page, now including a \<main\> semantic tag for better document outline.  
* **CSS3 (Tailwind CSS):** Used for styling, layout, and responsive design. It utilizes Tailwind CSS classes for rapid UI development, supplemented by custom CSS for specific aesthetic enhancements (e.g., custom fonts, shadows, and hover effects). Extensive styling is implemented for both dark and light themes to ensure visual harmony and readability across modes.  
* **JavaScript (ES6+):** Handles the dynamic behavior of the page:  
  * **DOM Manipulation:** Selects and updates elements on the page (e.g., displaying images, showing/hiding buttons, updating messages).  
  * **External API Integration:** Fetches the contribution graph image from https://ghchart.rshah.org/{username}. This service generates an SVG image based on the provided GitHub username.  
  * **Event Handling:** Listens for user interactions such as button clicks and key presses.  
  * **Image Loading:** Uses the Image object to asynchronously load the graph image and handle onload (success) and onerror (failure) events.  
  * **File Download:** Programmatically creates a temporary \<a\> element to trigger the download of the SVG image.  
  * **Theme Management:** Manages the dark/light mode toggle, applies the correct CSS classes to the \<body\> element, and saves the user's theme preference to localStorage.  
  * **Excluded Usernames:** Manages an array (excludedUsernames) to prevent specific users' graphs from being displayed, enhancing privacy.

### **Accessibility Features**

The application incorporates several accessibility features:

* **Semantic HTML:** Uses meaningful HTML5 elements like \<main\> to improve document structure for assistive technologies.  
* **ARIA Attributes:**  
  * aria-label is used on interactive elements (usernameInput, themeToggle) to provide clear, concise labels for screen reader users.  
  * aria-live="polite" on the graph-container ensures that dynamic content updates (like loading messages, error messages, or the graph itself) are announced to screen readers without interrupting the user.  
  * aria-hidden="true" is applied to decorative SVG icons within the theme toggle button to prevent screen readers from announcing redundant information.  
* **Alt Text for Images:** Dynamic alt attributes are provided for the contribution graph image, describing its content.  
* **Keyboard Navigation:** All interactive elements are reachable and operable via keyboard (e.g., using Tab to navigate and Enter to activate buttons/input).

### **File Structure**

The entire application is contained within a single ghart.html file, including HTML, CSS (both inline and via Tailwind CDN), and JavaScript.

### **Dependencies**

* **Tailwind CSS CDN:** Loaded directly from https://cdn.tailwindcss.com for utility-first styling.  
* **ghchart.rshah.org:** An external service used to generate and provide the SVG contribution graph images. The application relies on the availability and proper functioning of this service.

—

\> Generated by Google Gemini, refined by Duffin