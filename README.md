# Welcome to Kelly's Little Lemon API

## Get started

Start a terminal window in top level of this repo, and run each of the following:

`pipenv shell`
`pipenv install`
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py runserver`

## Access

Note: The admin user has full access to all functionality.

### Users
- Admin username: `superuser`
- Manager username: `Lemon`
- Crew username: `Sana`

Existing usernames are case-sensitive and just the user's name.

### Credentials
- Password (all existing users): `littlelemon123`

## Features
### Functionality requirements

1.	The admin can assign users to the manager group
    - **Endpoint:** */api/groups/manager/users/*
    - **Method:** `POST`
    - **Form fields:** *username*
    - **Additional functionality:** View list of Manager names (`GET`), remove user from group (`DELETE`)
2.	You can access the manager group with an admin token
    - **Endpoint:** */api/groups/manager/users/*
3.	The admin can add menu items
    - **Endpoint:** */api/menu-items/*
    - **Method:** `POST`
    - **Form fields:** *title*, *price*, *category*, *featured*
4.	The admin can add categories
    - **Endpoint:** */api/categories/*
    - **Method:** `POST`
    - **Form fields:** *title*, *slug*
5.	Managers can log in 
    - **Endpoint:** */api/token/*
    - **Method:** `POST`
    - **Form fields:** *username*, *password*
6.	Managers can update the item of the day
    - **Endpoint:** */api/menu-items/<id\>*
    - **Method:** `PATCH`
    - **Form field:** *featured*
    - **Additional functionality:** To find the current featured item, make a `GET` request to *api/menu-items/* with the query string *?featured=True*
7.	Managers can assign users to the delivery crew
    - **Endpoint:** */api/groups/crew/users/*
    - **Method:** `POST`
    - **Form fields:** *username*
    - **Additional functionality:** View list of Delivery crew names (`GET`), remove user from group (`DELETE`)
<!-- 8.	Managers can assign orders to the delivery crew -->
<!-- 9.	The delivery crew can access orders assigned to them -->
<!-- 10. The delivery crew can update an order as delivered -->
11. Customers can register
    - **Web registration path:** */api/register/*
12. Customers can log in using their username and password and get access tokens
    - **Token endpoint for access and refresh tokens:** */api/token/* to acquire access and refresh tokens (`POST` with *username* and *password* fields), */api/token/refresh* to use refresh token (`POST` with *refresh* field)
    - **Web login path:** */api/login/*
    - **Additional functionality:** Log out from web view at */api/logout/*
13. Customers can browse all categories 
<!-- 14. Customers can browse all the menu items at once -->
15. Customers can browse menu items by category
    - **Endpoint:** */api/menu-items/?category__title={{case-sensitive category title}}* (use */api/categories* to identify existing category titles)
    - **Method:** `GET`
<!-- 16. Customers can paginate menu items -->
17. Customers can sort menu items by price
<!-- 18. Customers can add menu items to the cart -->
<!-- 19. Customers can access previously added items in the cart -->
<!-- 20. Customers can place orders -->
<!-- 21. Customers can browse their own orders -->