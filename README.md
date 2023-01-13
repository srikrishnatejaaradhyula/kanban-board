# Kanban application

In the Kanban application, task management application . users can manage multiple tasks and create a list of tasks that can be deleted and updated further. Users can perform CRUD operations on lists, and cards, also there is a summary page where users can view their tasks in the form of graphs

### project folder
 📦kanban

 ┣ 📂template

 ┃ ┣ 📜card.html

 ┃ ┣ 📜card_edit.html

 ┃ ┣ 📜home.html

 ┃ ┣ 📜index.html

 ┃ ┣ 📜list.html

 ┃ ┣ 📜list_edit.html

 ┃ ┣ 📜login.html

 ┃ ┣ 📜register.html

 ┃ ┗ 📜summary.html

 ┣ 📜api_design.yaml

 ┣ 📜api.py

 ┣ 📜app.py

 ┣ 📜database.db

 ┗ 📜requirement.txt

 
## Requirement Installation

For install requirement Librarie execute the command. Given in the below in terminal are in command prompt.

```pip3 install -r requirement.txt```

## Execution of Python file

After install requirement Librarie . Run app.py python file

>Directory of the terminal should be the same directory of the project

``` python  ../kanban/app.py```

> Note : no need to run api.py python file it automatically executive in app.py. so,no need of separate execution.

After execution you can see  similar kind of output in terminal
```
     * Serving Flask app 'app'
     * Debug mode: on
     * Running on http://127.0.0.1:5000
        Press CTRL+C to quit
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 145-446-769
 ```
 Press CTRL + C  or copy and paste it on browser the folloing url

``` http://127.0.0.1:5000```

> Note : make sure, active Internet connection.

> Use api_design.ymal file for api

## screenshots

![index](https://drive.google.com/uc?export=view&id=1sOTWIJfVPJjG0lBE5GTazfRBJ7wl4wkt)

#### login page
 ![login page](https://drive.google.com/uc?export=view&id=1UZ6cY5e7hoqvR9KIQHagtQj6oIoaeF84)
####  signup page
 ![signup page](https://drive.google.com/uc?export=view&id=1M8ZGf95fkghdyHK7RmJOS2ag6XjKxGhL)
#### home page
 ![home page](https://drive.google.com/uc?export=view&id=1qSCz_wjMVy3qBPZN7Qj1yha8BMjRxU6Y)
#### list
 ![list page](https://drive.google.com/uc?export=view&id=1Z6OjoTF--EAQpHnUgI_M0iZ7cBChX5YD)
 
#### card
 ![card page](https://drive.google.com/uc?export=view&id=1-GJI7tOVnSTjx7hxvow6ykEJ9vHfxpzd)
#### summary page
 ![summary page](https://drive.google.com/uc?export=view&id=1vALP3ZtvI44gC8fel9amHaTSiB64he8Q)
 


