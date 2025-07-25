# **LocalHub Documentation**

LocalHub is a robust, private, and fully functional local version of a Git-like repository manager, designed for personal use directly within your web browser. It leverages your browser's LocalStorage to securely manage your code snippets, text files, and other data without the need for external servers or complex setups.

## **Key Features**

* **Local Repository Management:** Create, view, and manage multiple repositories directly in your browser's local storage.  
* **File Operations:** Within each repository, you can:  
  * Add new files with custom names and content.  
  * View the content of existing files.  
  * Edit the content of existing files.  
  * Delete files.  
* **Persistent Storage:** All your repositories and files are saved in your browser's LocalStorage, meaning your data persists even after you close and reopen the browser tab or window.  
* **Theme Toggle:** Switch between a light and dark mode to suit your visual preference. Your theme choice is saved locally.  
* **Data Import/Export:**  
  * **Export:** Download all your LocalHub data as a single JSON file for backup purposes.  
  * **Import:** Load existing LocalHub data from a JSON file, allowing you to restore or transfer your repositories.  
* **Real-time Statistics:** Keep track of your total repositories, files, and the amount of local storage used by LocalHub.  
* **Accessibility Features:**  
  * **Semantic HTML:** Uses appropriate HTML5 elements like \<main\> for better screen reader navigation.  
  * **ARIA Attributes:** Modals are enhanced with role="dialog" and aria-modal="true" for improved screen reader context.  
  * **Focus Management:** When modals open, focus is automatically shifted to the modal, and it returns to the triggering element upon closure.  
  * **Keyboard Navigation:** Modals support closure via the Escape key and proper tab trapping for keyboard-only users.

## **How to Use LocalHub**

### **Creating a New Repository**

1. In the "Create New Repository" section, enter a unique name for your repository in the input field.  
2. Click the "Create Repository" button.  
3. Your new repository will appear in the "Your Repositories" list.

### **Managing Files within a Repository**

1. Click on a repository name in the "Your Repositories" list to open it.  
2. **Add/Edit File:**  
   * Enter a file name in the "File Name" input.  
   * Enter your content in the "Content" textarea.  
   * Click "Add File" to save a new file or overwrite an existing one (you'll be prompted for confirmation if overwriting).  
3. **View File Content:**  
   * Click on a file name in the "Files" list. Its content will be displayed in the "File Content Preview" area below. The file name and content will also load into the "Add/Edit File" section for quick editing.  
4. **Save Changes to an Existing File:**  
   * After clicking a file to view it, its content will appear in the "Add/Edit File" section. Make your changes in the textarea.  
   * Click the "Save Changes" button (which appears when a file is selected for editing).  
5. **Delete a File:**  
   * Click the "Delete" button next to the file you wish to remove from the "Files" list. You will be asked for confirmation.

### **Navigating Back**

* Click the "Back to Repositories" button within a repository's view to return to the main list of your repositories.

### **Exporting/Importing Data**

* **Export Data:** Click the "Export Data" button in the "Stats" section to download a JSON file containing all your LocalHub data.  
* **Import Data:** Click the "Import Data" button and select a localhub\_backup.json file. Be aware that importing data will **overwrite** your current LocalHub data.

### **Toggling Theme**

* Click the sun (☀️) or moon (🌙) icon in the top-right corner to switch between light and dark modes. Your preference will be saved for future visits.

## **Technical Notes**

* **LocalStorage:** LocalHub stores all its data directly in your web browser's LocalStorage. This means your data is private to your browser and is not uploaded to any server.  
* **Storage Limits:** LocalStorage typically has a size limit of 5-10MB per website. While sufficient for many text-based files, be mindful of this limit if storing very large amounts of data. The "Local Storage Used" statistic helps you monitor this.  
* **Security:** Content displayed in the "File Content Preview" is rendered within a \<pre\> tag, which prevents the execution of embedded HTML or JavaScript, ensuring safety against most common injection attacks (XSS).  
* **Styling:** LocalHub utilizes Tailwind CSS for its responsive and modern design.

## **Important Note**

LocalHub is intended for users already familiar with concepts of version control systems like GitHub. It provides a local sandbox environment for managing your personal code and files.