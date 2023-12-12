# Little Lemon API (Django REST Framework Practice Project)

This is the capstone project for the [Meta Back-End Developer Professional Certificate](https://www.coursera.org/professional-certificates/meta-back-end-developer) course "APIs", built using the Django REST Framework.

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

Usernames are case-sensitive.

### Credentials
- Password (all existing users): `littlelemon123`

## Features
### Functionality requirements

1.	The admin can assign users to the manager group
    - **Endpoint:** */api/groups/manager/users/*
    - **Method:** `POST`
    - **Form fields:** `username`
    - **Additional functionality:** View list of Manager names (`GET`), remove user from group (`DELETE`)
2.	You can access the manager group with an admin token
    - **Endpoint:** */api/groups/manager/users/*
    - **Note:** For endpoints requiring auth tokens for access, the token prefix is "Bearer"
3.	The admin can add menu items
    - **Endpoint:** */api/menu-items/*
    - **Method:** `POST`
    - **Form fields:** `title`, `price`, `category`, `featured`
4.	The admin can add categories
    - **Endpoint:** */api/categories/*
    - **Method:** `POST`
    - **Form fields:** `title`, `slug`
5.	Managers can log in 
    - **Endpoint:** */api/token/*
    - **Method:** `POST`
    - **Form fields:** `username`, `password`
6.	Managers can update the item of the day
    - **Endpoint:** */api/menu-items/<id\>*
    - **Method:** `PATCH`
    - **Form field:** `featured`
    - **Additional functionality:** `featured` is the only `MenuItem` field Managers are allowed to update. When an item is set to `featured`, the current featured item (if there is one) has its `featured` field set to `False`.
7.	Managers can assign users to the delivery crew
    - **Endpoint:** */api/groups/crew/users/*
    - **Method:** `POST`
    - **Form fields:** `username`
    - **Additional functionality:** View list of Delivery crew names (`GET`), remove user from group (`DELETE`)
8.	Managers can assign orders to the delivery crew
    - **Endpoint:** */api/orders/<id\>*
    - **Method:** `PATCH`
    - **Form field:** `delivery_crew`
    - **Note:** `delivery_crew` field uses user id. Adrian (id 4) and Sana (id 6) are existing users assigned dto the Delivery crew group. 
    - **Additional functionality:** `delivery_crew` is the only `Order` field Managers are allowed to update. `status` has a default of "pending" if there is no `delivery_crew`, and automatically updates to "assigned" when a `delivery_crew` is set. Managers may view all orders at */api/orders/*.
9.	The delivery crew can access orders assigned to them
    - **Endpoint:** */api/orders/*
    - **Method:** `GET`
    - **Additional functionality:** Delivery crew can see only the orders assigned to them.
10. The delivery crew can update an order as delivered
    - **Endpoint:** */api/orders/<id\>*
    - **Method:** `PATCH`
    - **Form field:** *status*
    - **Additional functionality:** `status` is the only `Order` field Delivery crew are allowed to update, and they can only change the value to "delivered" as "pending" and "assigned" are set automatically.
11. Customers can register
    - **Web registration path:** */api/register/*
12. Customers can log in using their username and password and get access tokens
    - **Token endpoint for access and refresh tokens:** */api/token/* to acquire access and refresh tokens (`POST` with `username` and `password` fields), */api/token/refresh* to use refresh token (`POST` with *refresh* field)
    - **Web login path:** */api/login/*
    - **Additional functionality:** Log out from web view at */api/logout/*
13. Customers can browse all categories
    - **Endpoint:** */api/categories/*
    - **Method:** `GET`
14. Customers can browse all the menu items at once
    - **Endpoint:** */api/menu-items/*
    - **Method:** `GET`
    - **Note:** The *menu-items/* endpoint shows all results by default. To paginate, add a page query *(?page={{page number}})* to the request.
15. Customers can browse menu items by category
    - **Endpoint:** */api/menu-items/?category={{category title}}*
    - **Method:** `GET`
16. Customers can paginate menu items
    - **Endpoint:** */api/menu-items/?page={{page number}}*
    - **Note**: While staff see browsable JSON, customers and users not logged in see a template with page buttons. The buttons work in a web browser by updating the query string in the url, but if you are using an API client like Insomnia instead of a web browser you need to manually set the page query *(?page={{page number}})* in the request.
17. Customers can sort menu items by price
    - **Endpoint:** */api/menu-items/?sortby=price* (or *=-price* for ascending prices)
18. Customers can add menu items to the cart
    - **Web browser endpoint (template view):** */api/menu-items/*
    - **Web browser action:** Click "Add to cart".
    - **API endpoint:** */api/cart/*
    - **API methods:** `POST`, `DELETE`
    - **API field:** `menu_item_title`
    - **Additional functionality:** Customers can remove items from their cart by placing a `DELETE` request to */api/cart/* with a `menu-item_title` identifying the item to be removed.
<!-- 19. Customers can access previously added items in the cart -->
<!-- 20. Customers can place orders -->
21. Customers can browse their own orders
    - **Endpoint:** */api/orders/*
    - **Method:** `GET`
    - **Additional functionality:** Customers can see only their own orders.