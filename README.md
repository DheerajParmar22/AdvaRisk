The Midnight Times: Building a News Search Web Application
- Dheeraj Parmar | parmardheeraj6@gmail.com | 9413802811


Objective:
Build a customer-facing web-based application that allows users to search for news articles
based on keywords and view the results of their previous searches. The application uses the
News API to fetch news articles and provides a user-friendly interface to interact with the data.


Setup Instructions:
1. Clone the project repository from GitHub.
2. Install the required dependencies using pip install -r requirements.txt.
3. Configure the News API key in the settings.
4. Apply migrations using python manage.py migrations/migrate.
5. Create a superuser using python manage.py createsuperuser.
6. Run the development server using python manage.py runserver.


Modules/Methods Documentation:

views.py:
● loginPage(request): Handles user login, authentication, and redirects to the search page
upon successful login.
● logoutUser(request): Logs out the authenticated user.
● registerUser(request): Handles user registration, account creation, and redirects to the
search page upon successful registration.
● search(request): Handles user search queries, stores search results, and allows filtering
by date, source, and language.
● search_results(request, search_id): Displays the search results along with options to
filter by date, source, and language.
● refresh_results(request): Fetches and stores new search results for a keyword, updating
the existing ones.
● delete_search(request, search_id): Allows the user to delete a search and associated
results.
● userProfile(request, pk): Displays the user profile page.

models.py:
● UserSearch: Represents a user's search query and related metadata such as keyword
and date searched.
● SearchResult: Represents a single news article result associated with a user's search
query.

admin.py:
● CustomUserAdmin: Customizes the admin interface for the built-in User model, adding
actions to block and unblock users.
● UserSearchAdmin: Customizes the admin interface for the UserSearch model,
displaying search history and trending keywords.
External Libraries/Classes Used:
Please find enclosed the 'requirements.txt' file, where I've taken the liberty of
meticulously reviewing and including the essential libraries only from my personal
system. I've also added a few extra libraries just in case they might come in handy.
Should you require any further adjustments or insights, please contact me anytime.
I want to make sure everything works smoothly for you!
Implementation Highlights:
● Implemented a user-friendly interface allowing users to search for news articles based
on keywords.
● Stored search results and provided options to filter and sort them.
● Integrated user authentication, registration, and profile pages.
● Added admin actions to block/unblock users and view trending keywords.
Challenges Faced:
● Configuring the News API integration.
● Setting up background job scheduling using Celery.
● Customizing the admin interface to display relevant data and trends.


Total Time Taken:
The project was completed over a span of 3 days, with around 5-6 hours spent each day.


Overall Experience:
Working on this project was a great experience. It allowed me to apply Django concepts,
manage APIs, and build a real-world application. The project exposed me to challenges related
to data fetching, user authentication, and admin customization. I learned valuable skills in web
development, API integration, and using Django's built-in features effectively.


Conclusion:
This project successfully accomplished the objectives of building a news search web application
with features such as user authentication, search history, result filtering, and admin controls. It
was an opportunity to showcase skills in Django development, API integration, and delivering a
user-friendly interface.
