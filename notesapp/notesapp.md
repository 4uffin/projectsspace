# **Old School Notebook Notes App Documentation**

## **Project Overview**

The "Old School Notebook Notes App" is a simple, browser-based note-taking application designed to evoke the nostalgic feel of a physical notebook. It allows users to create, save, select, pin, and delete notes directly within their web browser, utilizing local storage for data persistence. The application features a clean, minimalist design inspired by traditional paper and ink, with a focus on usability and accessibility.

## **Key Features**

* **Create New Notes:** Easily add new blank notes to your collection.  
* **Save Notes:** Automatically saves note titles and content as you type or when focus is lost.  
* **Select Notes:** Click or use keyboard navigation to select and view existing notes.  
* **Pin/Unpin Notes:** Pin important notes to the top of the sidebar list for quick access.  
* **Delete Notes:** Remove unwanted notes with a confirmation step to prevent accidental deletion.  
* **Local Storage Persistence:** All notes are saved directly in your browser's local storage, meaning your notes will be there even after closing and reopening the browser.  
* **Responsive Design:** The application adapts its layout for optimal viewing and usability on various screen sizes, from desktop to mobile devices.  
* **Custom Confirmation Modal:** Provides an in-app confirmation dialog for deleting notes, enhancing user experience.  
* **Accessibility Features:** Includes a "Skip to content" link and keyboard navigation support for improved usability.

## **How to Use**

1. **Add a New Note:** Click the "Add Note" button in the sidebar. A new, empty note will appear in the editor area, and a "New Note" entry will be added to your notes list.  
2. **Enter Title and Content:** Type your note's title in the "Title" input field and your note's content in the "Note" textarea. Changes are automatically saved as you type or when you click/tab away from the fields.  
3. **Save Note:** You can explicitly click the "Save Note" button, or simply move focus away from the title/content fields, and your changes will be saved.  
4. **Select a Note:** Click on any note title in the "Notes" sidebar to load its content into the editor. You can also use the Tab key to navigate through the note items and press Enter or Space to select a note.  
5. **Pin/Unpin a Note:** With a note selected, click the "Pin Note" button. The note will be marked with a 📌 icon and moved to the top of the notes list. Click the button again (which will now say "Unpin Note") to unpin it.  
6. **Delete a Note:** Select the note you wish to delete and click the "Delete Note" button. A confirmation modal will appear; click "Yes, Delete" to confirm or "Cancel" to keep the note.

## **Technical Details**

The application is built using standard web technologies:

* **HTML5:** Provides the structure and content of the webpage.  
* **CSS3:** Styles the application, including the "lined paper" effect for the editor, responsive layouts, and visual transitions.  
* **JavaScript (Vanilla JS):** Handles all the interactive logic, including:  
  * Managing note data in a JavaScript array.  
  * Interacting with localStorage for data persistence (localStorage.setItem, localStorage.getItem).  
  * Dynamically rendering and updating the notes list.  
  * Implementing event listeners for user interactions (clicks, keydowns, blur).  
  * Creating and managing the custom confirmation modal for deletions.

### **Key Implementations:**

* **Data Storage:** Notes are stored as an array of objects in localStorage, each object containing an id, title, content, and pinned status.  
* **Responsive Design:** Achieved using CSS Flexbox for the main layout and @media queries to adjust the layout for smaller screens, stacking the sidebar and editor vertically.  
* **Custom Modal:** A custom HTML structure is used for the modal, controlled by JavaScript to show/hide it and handle user input, replacing the browser's native confirm() function for a more integrated experience.  
* **Accessibility:** Semantic HTML, role attributes, tabindex for keyboard navigation, and a "skip-link" are used to enhance accessibility.