
# Eat Vegan Recipes
## Code Institute: Milestone Project 3 - Jamie Rolls
---
![Desktop](documentation/responsive-screenshots.png)

Eat Vegan Recipes is a recipe site dedicated to Vegan food, the recipes are added by and reviewed by the sites visitors. The site is designed to be easy to navigate, promoting a simple layout with minimal but effective and purposeful features. 

#### **Project Requirements:**
Build an interactive front-end website that responds to user actions and alters the way the site displays data/information.

Required Technologies : HTML, CSS, JavaScript, Python+Flask, MongoDB.
Optional: Include use of JQuery, other Javascript libraries and external APIs.

A live version of the site is available [here.](https://ms3-eat-vegan-recipes.herokuapp.com/)

# Table of Contents

# Strategy and Scope
## UX

#### Business Objectives

- The site will attract users seeking Vegan recipes which are tried and tested by others. As a community contributed site, it is expected that recipes which are shared have been verified.
- The site should make it easy for its users to add recipes, leave reviews for others and verify/like other recipes.
- The site will have filter and search functions to support ease of use and site navigation.
- Social media channels will be linked on all pages, to build a community following on other 'Eat Vegan Recipes' platforms.

#### User Objectives

- Users will be looking for recipes in the every growing Vegan food movement. Recipes are desired for different meals throughout the day.
- A user may want to share a favorite recipe with others, this should be easy to complete with little hassle.
- Users may have want to search for a recipe, they use Eat Vegan Recipes due to the ever growing recipe list and the supporting reviews/votes system in place for recipes.


#### Project Goals

- Create a clear, well designed website for the user to navigate with ease.
- Use a consistent, clear theme throughout the site.
- Consider appropriate pages/layout and content to fulfil business/user objectives.
- Integrate a database into the webapp using MongoDB + Flask, the database will store recipes, reviews and other supporting information.
- Consider user authentication, to allow users to edit their own recipes if desired.
- Fulfil all mandatory project requirements as a minimum. (these are listed below)

#### Mandatory Requirements

1. Data handling: Build a MongoDB-backed Flask project for a web application that allows users to store and manipulate data records about a particular domain. If you are considering using a different database, please discuss that with your mentor first and inform Student Care.
2. Database structure: Put some effort into designing a database structure well-suited for your domain. Make sure to put some thought into the nesting relationships between records of different entities.
3. User functionality: Create functionality for users to create, locate, display, edit and delete records (CRUD functionality).
4. Use of technologies: Use HTML and custom CSS for the website's front-end.
5. Structure: Incorporate a main navigation menu and structured layout (you might want to use Materialize or Bootstrap to accomplish this).
6. Documentation: Write a README.md file for your project that explains what the project does and the value that it provides to its users.
7. Version control: Use Git & GitHub for version control.
8. Attribution: Maintain clear separation between code written by you and code from external sources (e.g. libraries or tutorials). Attribute any code from external sources to its source via comments above the code and (for larger dependencies) in the README.
9. Deployment: Deploy the final version of your code to a hosting platform such as Heroku.
10. Make sure to not include any passwords or secret keys in the project repository.


#### User Stories

1. As a visitor to the site, I want to easily find a recipe for lunch and for dinner. The recipe should have reviews.
2. As a visitor to the site, I want to share one of my favorite vegan recipes with others.
3. As a visitor to the site, I want to search for a light snack to make for some Vegan friends.
4. As a previous visitor to the site, I want to edit a recipe that I added to the site on a previous visit.
5. As a previous visitor to the site, I want to review a recipe that I cooked last week. It would be good to be able to search for the recipe, as I remember the name of it.


# Structure

## Design Process

#### Page Structure

* The site is designed to remain simple and stylish throughout, most of the navigation will be completed via call to action buttons. An optional navbar will be collapse at the top right of each screen, containing links to key pages and search filters. 
 This design choice will support a primary user journey of locating a recipe quickly which is suited to the user.

* Elements from a Start Bootstrap theme were customised and utilised accross the site. The theme can be found here: ------ . The simplicity and effectiveness of the call to action buttons were supportive of my decision to use this theme as part of 'Eat Vegan Recipes'

* Research on recipe page layouts was conducted accross various food and recipe websites, this information has inspired and aided my decisions on page design for individual recipes. The purpose was to display content clearly, which is easy to read on different devices. As recipes may be viewed whilst cooking, this is an important consideration.

* I began to outline the content requirements for the site and thought about the best way for a user to navigate through this content.

* The following pages were chosen to be created: 
    - Home (landing page)
    - All recipes (with search and filter buttons)
    - Individual recipe page
    - Submit Recipe form

* A collapsed nav bar containing links to a the following will be present on all pages in the top righthand corner of the screen:

- All Recipes
- Breakfast Recipes
- Lunch Recipes
- Dinner Recipes
- Dessert Recipes
- Add Recipe
- Login / Sign Up
- Social Media Icons

#### Home - landing page

* The landing page has four main sections followed by the footer. 

    1. Header, spanning the full viewport. Consisting of a relevant background image. website logo, site name, call to action button (link to next section on page)
    2. Top four rated recipes (these will be dynamic, displaying the four reciped from the databasw with the highest votes)
    3. Recipe links - Four links to show recipes from different categories - these will open a new page.
    4. A call to action button - allowing users to add their own recipe - This will require authentication/login to access the submit recipe page.

#### All Recipes Page

* The all recipes page (get_recipes.html) will dynamically show recipes from the database, depending on search terms or filters which have been applied. There will be four sections on the page followed by the footer. 

    1. Header - reduced size, to contain the site name and the collaped navbar link.
    2. Recipe search and filters section.
    3. Recipe cards, with overlaid text (name, short description, votes)
    4. A call to action button - allowing users to add their own recipe - This will require authentication/login to access the submit recipe page.

#### Individual Recipe Page

* The individual recipe page will display a single recipe from the database, the recipe would have been selected from the 'All recipes page'. This page will display all recipe data from the database. There will be four main sections followed by the footer. 

    1. Header - reduced size, to contain the site name and the collaped navbar link.
    2. Recipe - Header, image and short description. Followed by ingredients and method.
    3. Reviews - Display reviews which have been left by other users - which are related to this recipe.
    4. Two call to action buttons - 
        - Button linking to the submit recipe form page. This will require authentication/login to access.
        - Button linking the user back to the 'All recipes' page.

#### Submit Recipe Page

* This page consist of three sections followed by the footer.

    1. Header - reduced size, to contain the site name and the collaped navbar link.
    2. Recipe submission form - This will contain all fields required to fulfil a recipe entry in the database. Fields will be required and the form will provide user feedback to ensure it is filled correctly. A submit button will be present at the end of the form, which pushes the inputs to the database.
    3. A call to action button linking the user back to the 'All recipes' page.


# Skeleton

## Wireframe designs

Wireframes were designed using Balsamiq, for three primary breakpoints - Desktop, Tablet and Mobile.

- Desktop Wireframes.

![Desktop - ](https://github.com/jamie120/ms3-eat-vegan-recipes/blob/master/documentation/wireframes/Desktop.png "Desktop - Wireframe screenshot")

- Tablet Wireframes.

![Tablet - ](https://github.com/jamie120/ms3-eat-vegan-recipes/blob/master/documentation/wireframes/Tablet.png "Tablet - Wireframe screenshot")

- Mobile Wireframes.

![Mobile - ](https://github.com/jamie120/ms3-eat-vegan-recipes/blob/master/documentation/wireframes/Mobile.png "Mobile - Wireframe screenshot")


## Wireframe and Final Project Differences

- Home Page
    - Recipe page links are in a single row on mobile - containing all four links. As opposed to opting for a single row per link. This was decided to assist the user experience by reducing the need to scroll excessively.
- Recipes
    - Recipe filter links and icons on tablet and mobile remain in a single row, as is on the desktop Wireframe. This was found to improve the look of the site and maintain consistency between screen sizes. 
- Recipe Page
    - The recipe page on desktop adopts a more simple layout, which compliments the site design. The recipe image occupies the top of the page on a single row. All recipe information follows the image. 
- Add Recipe form
    - The form is now displayed on desktop, as it is on tablet and mobile wireframes. This design choice supports the site design and it was found the additional column in the wireframe design was not required to display information.
- Navbar
    - The navbar adopted a minimalistic design, the recipe types have been collapsed under a single link 'recipes'. Which can be expanded to display the additional links when desired. 
    - Login / Register links added, displayed accordingly.
    - Add recipe link, displayed accordingly.

## Responsive Page Design

The site has been designed to operate well on all screen sizes. As a core purpose of the site is to host recipes, it is expected that the site will be viewed on tablet and mobile devices often, whilst in the kitchen. With that in mind, the site content and layouts have been designed to support a positive user experience.

- Page Header
    - Fontsize and header height is reduced on smaller devices to ensure best use of space is acheived.
- Home page
    - The top four recipes are displayed in a single column on tablet and mobile.
    - The links to the 'recipes' page are displayed in a single row on desktop and mobile. On tablet to make best use of the space, the links are displayed over two rows.
- Recipes
    - The recipe cards are displayed in rows of three on desktop, this is reduced to a single recipe card per row for tablet and mobile size screens.
    - Recipe card pagination is set to 6 recipes per page, to reduce loading times and improve the user experience.
- Recipe Page
    - The recipe information stacks on tablet and mobile devices.
    - The edit and delete recipe buttons stack below the recipe 'like' info, on mobile devices.
    - The delete comment button, stacks below corresponding comments, if applicable. On mobile devices.
- Edit / Add recipe page
    - Padding and margin is adjusted on smaller screen sizes to maintain form conformity and a positive user experience.


## Database Design and structure

* The database 'eat_vegan_recipes' will consist of three collections. Compiled and hosted using [MongoDB](https://www.mongodb.com/) Recipes & Reviews. 

### Recipe Structure
1. _id - ObjectId - (generated by mongoDB)
2. name - str
3. category - str 
4. short_description - str
5. recipe_info - array
6. ingredients - array
7. method - str
8. img_url - str
9. votes - int
10. added_by - str

### Reviews Structure
1. _id - ObjectId - (generated by mongoDB)
2. recipe_review - str
3. recipe_rating - str
4. recipe_id - str
5. added_by - str

### Users

1. _id - ObjectId - (generated by mongoDB)
2. username - str
3. password - str - (password hash generated by werkzeug.security)

# Surface

## Colours

Colour Palette - Three main colours that compliment the design of the site are:

 - ![#2c4650](https://via.placeholder.com/15/2c4650/000000?text=+) - `#2c4650` - Section background
 - ![#343a40](https://via.placeholder.com/15/343a40/000000?text=+) - `#343a40` - Dark section background
 - ![#1D809F](https://via.placeholder.com/15/1D809F/000000?text=+) - `#1D809F` - Page buttons, navbar
 - ![#f8f9fa](https://via.placeholder.com/15/f8f9fa/000000?text=+) - `#f8f9fa` - Page buttons
 - ![#ecb807](https://via.placeholder.com/15/ecb807/000000?text=+) - `#ecb807` - Page fonts

* Other various shades of grey are used to highlight, surround and drop shadows on elements throughout the site.

## Font Choice

The following fonts were applied to the site. 

- Gloria Hallelujah
- Thasadith
- Monospace
- Source Sans Pro (default font - applied to body)

Gloria Hallelujah and Thasadith were obtained through Google Fonts. They are imported from 'Google Fonts' in the customer style.css file. 


Readme notes:


Sources used:

RANGE BUBBLE FOR RECIPE RATING - https://css-tricks.com/value-bubbles-for-range-inputs/

MONGODB Documentation - https://docs.mongodb.com/

Bootstrap Documentation - https://getbootstrap.com/docs/4.0/getting-started/introduction/

Start Bootstrap - https://startbootstrap.com/ - Used for page elements and inspiration from themes and templates.


Images - 

Recipes - Unsplash:

Avacado Pitta - https://unsplash.com/photos/MAbhhj3QCXQ - @atasteofwellbeing

Vegan Burger - https://unsplash.com/photos/kPLccIMtS8E - @runningonrealfood

Buddah Bowl - https://unsplash.com/photos/IGfIGP5ONV0 - @annapelzer

Tofu Curry - https://unsplash.com/photos/PqsImnjuElM - @charlesdeluvio

Red Lentil Dahl - https://unsplash.com/photos/gVOvZFcYBMY - @edgarraw

Pistaccio Ice-cream - https://unsplash.com/photos/alEZLDPPRBU - @aribes

Landing Page - Unsplash - https://unsplash.com/photos/Ww8eQWjMJWk - @hermez777

Fish and chips - https://unsplash.com/photos/hfK401V_NXk - @jannerboy62