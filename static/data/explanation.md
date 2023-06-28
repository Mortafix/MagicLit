### Introduction
This guide provides a comprehensive overview of the structure and functionality of our project. It aims to **assist** users in understanding the main components and their interactions. With its main script, organized pages, menu files, components and fragment functionality, this project offers a different and user-friendly way to use Streamlit. The project is primarily driven by the `app.py` main script, which serves as the central hub for all operations. Enjoy the journey!

### Main Script: `app.py`
The `app.py` script contains the core logic of the project. It orchestrates various functionalities and handles crucial aspects of the application. Below are the key features of this script:

1. **Shared Static Resources**: This section includes static resources that are shared across multiple pages. It ensures consistent visual elements and enhances user experience.

2. **Query Parameters Handling**: The main script handles query parameters, allowing users to pass information through the URL. This functionality enables dynamic content generation and tailored user experiences.

3. **Fragment Management**: The script also manages the all-important fragment, allowing seamless navigation within the application. It ensures smooth scrolling and bookmarking of specific sections.

4. **CSS Styling**: The script incorporates both local and external CSS files to control the overall styling of the project. Additionally, it includes special CSS rules specific to individual pages, providing unique visual elements where needed.

5. **User Logging**: Finally, the script implements user login logic to facilitate authentication and access control to the platform. This ensures secure user interactions and protects sensitive information.

### Pages

Next, we have the `pages` directory, which allows for **logical division** of files. Subdirectories can be created to organize files based on specific criteria, such as subdomains within the same application. In this case, the main folder we are interested in is the `main` folder, which contains all the necessary files for the application.

The structure of the application with multiple pages is defined by the menu logic, which will be explained in the following section. The `pages` directory serves as a container for all the relevant files that make up the application, ensuring a clear and organized arrangement of the project's components.

### Menu

All the menu-related files can be found in the `utils > menu` folder. Within this folder, there are primarily **3** important files that contribute to the menu's functionality and structure:

1. **Menu File**: This file represents the actual menu and allows for the representation of various sections and pages within the application. It serves as a visual representation of the app's navigation structure, providing an intuitive user interface. Detailed explanations of the menu's contents can be found below.

2. **Page-to-Script Mapping**: This file establishes the mapping between the pages specified in the previous file and the corresponding Python scripts or functions to be executed when each page is accessed. It ensures the proper execution of the necessary code based on the selected page.

3. **Parser**: The parser file acts as a communication bridge between the two aforementioned files. It enables the synchronization of the menu file's representation and the corresponding Python scripts, ensuring a seamless connection between the user interface and the backend functionality.

These three files work together to define the menu's structure, associate pages with their respective scripts, and establish a coherent communication flow within the application.

#### Menu Formatting
> You can find an example (for this app) in `utils > menu > app.menu`

In the `utils > menu` folder, the menu-related file follow a specific format using symbols to convey information:

- Lines beginning with `*` represent a **section**.
- Lines beginning with `-` indicate the **pages** within that section.
- Lines beginning with `+` represent **extra pages**, outside of the normal menu structure (free pages).

Within each line, you will find the following symbols and their corresponding meanings:

- `:` followed by the **icon**'s name (using [Google's Material Icons](https://fonts.google.com/icons?icon.set=Material+Icons)).
- `@` followed by the **internal page name** (used by the mapping script to determine which script to execute and to reference the page within the app).
- `#` denotes the **category** to mark as active (only for free pages).

Additional symbols can be used to indicate extra parameters for sections and pages:

- `!` indicates that the section or page is only accessible by **admins** and will be hidden from regular users.
- `/` is used to **hide** a page or section from all users.
- `?` indicates that a page is under **development**, and there will be a _coming soon_ label displayed alongside it.
- `1` indicates that the page will be the **initial page** shown upon login (there can only be one).

### Components

When it comes to **components**, there isn't much to explain in this section. It is recommended to refer to the individual pages of each component for a detailed understanding of their logic and implementation. These pages specify the scripts to be examined to comprehend the component's functionality and implementation.

By referring to the respective component pages, you will gain insights into the specific scripts and code responsible for the logic and behavior of each component. This approach allows for a deeper understanding of how the components are designed and implemented within the project.

### Fragment

The **main power** of the app lies in its **fragment** functionality, which enables fast page refresh. To understand its workings, it is recommended to examine the commented script located in `utils > web > fragment`. This script provides the implementation details of the fragment functionality.

The primary functioning can be simplified in the following format:

```
#func-name@param=1&param2
```

This format combines the _anchor_ of the URL with the _parameters_ from the query parameters. The usage logic involves invoking specific functions with their respective parameters based on the requested fragment.

It is important to note that the fragment component is delicate and should be used sparingly, despite thorough testing. 

> **CAUTION**: A known bug occurs after invoking a fragment and then clicking a regular button (non-form submitter). Since nothing is saved within the session_state, there is no way to determine when a button has been clicked, resulting in the fragment restarting (assuming it has been called).

### Miscellaneous Notes

Here are some additional notes regarding the project:

- The **CSS files** include more than what is strictly necessary for the app. They have been imported from the main project, and removing unnecessary styles would be time-consuming.
- Pages categorized under `SuperHero` serve a partial purpose. They are primarily used to showcase the functionality of **special CSS** styles (found in `static > css > special`) with titles displayed in various colors.
- The **database** used in the project is _MongoDB_, but it is not utilized within this specific context. If you wish to explore the database logic, it can be found in `utils > database > mongo`.
- You can optimize the app's performance further by modifying the _Streamlit_ configuration in `.streamlit > config.toml`. Notably, the following parameters can enhance speed:
```toml
[runner]
fastReruns = true

[server]
headless = true
enableStaticServing = true
```
- Customize the **color scheme** of the application by modifying the values in the `.streamlit > config.toml` file and the `static > css > colors.css` file. These files define the colors used throughout the application.