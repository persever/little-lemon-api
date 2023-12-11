# Welcome to Kelly's Little Lemon API

## Get started

Start a terminal window in top level of this repo, and run each of the following:

`pipenv shell`
`pipenv install`
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py runserver`

## Functionality requirements
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
<!-- 6.	Managers can update the item of the day
    - **Endpoint:** */api/menu-items/<id\>*
    - **Method:** `PATCH`
    - **Form field:** *featured*
    - **Additional functionality:** To find the current featured item, make a `GET` request to *api/menu-items/* with the query string *?featured=True* -->
<!-- 7.	Managers can assign users to the delivery crew -->
<!-- 8.	Managers can assign orders to the delivery crew -->
<!-- 9.	The delivery crew can access orders assigned to them -->
<!-- 10. The delivery crew can update an order as delivered -->
<!-- 11. Customers can register -->
<!-- 12. Customers can log in using their username and password and get access tokens -->
<!-- 13. Customers can browse all categories  -->
<!-- 14. Customers can browse all the menu items at once -->
<!-- 15. Customers can browse menu items by category -->
<!-- 16. Customers can paginate menu items -->
<!-- 17. Customers can sort menu items by price -->
<!-- 18. Customers can add menu items to the cart -->
<!-- 19. Customers can access previously added items in the cart -->
<!-- 20. Customers can place orders -->
<!-- 21. Customers can browse their own orders -->