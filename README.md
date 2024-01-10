# KUNTO
#### Video Demo:  <URL https://youtu.be/QmhyGFvBZ2E>
#### Description:
The web applocation is about the 100 day of code challinge, i start this challing on twitter since i start the cs50x course, now iam in day 82. The resone whay i make my idea on this is to make it easy to access my achivment and see the history, becouse in twitter you can uploade more then one tweet on diffrent topic, so i made this APP to fix this problem

feature of my app :
- Register / Login
- save your achivment on database
- count the days you eas working in
- see the history of yout achivment

app.py :
    its the flask file. has the functuion and pages route, i will explain every route here:

    Home - "/" :
        - take you to home page.
        - linked to home.html
            has the design of home page of webapp

    profile - "/profile" :
        - has the ability to get usernam and day count from database
        - this page give you information about your self and give you ability to change your username and password

            changeUser - "/changeUser" :
                - if the new user name was exect the username will not change and error message will desplay

            changePass - "/changePass" :
                - route to change the password

        - it connect with ( profile.html , layout.html , style.css )

    login - "/login" :
        - it check if the username is enterd or not, if not the system will return error message, also if the username not exict in database it will be return error message

        - ensure that the password was enterd, if not i will return error message.
            - if username was found the system will encypte the password and check if its same as the password in the database

        - if the password and username enterd was same as the one in the database the system will allow you to enter the web app and will remeber that you loged in with this username, and then will redirect you to home page

        - it connect with ( login.html , layout.html , style.css )

    register - "/register" :
        - ensure that the forms was enterd if not it will return error message

        - if forms was enterd the system will check if the username was in the database or not, if not the system will encybt the password and store it with the username in the database,otherwise the system will return error message

        - when you oress register the system will save your session

        - it connect with ( register.html , layout.html , style.css )

    MyDocument - "/MyDocument" :
        - check the day count and display the day in the page.

        ADD - "/ADD" :
            - if the user press this butten all the words written in  the forms will be saverd on the database and the DAYs table will be updated, if the form has no value it will have a defult value.

        RESTART - "/RESTART" :
            - If you click this butten all the data in achive table will be deleted

        - it connect with ( mydocument.html , layout.html , style.css )

    logout - "/logout" :
        - this choise will be seen if you loged in and if you click it, it will loged you out.

        - it connect with ( layout.html , style.css ) and you can see it in all pages if you was loged in.

    changePass - "/changePass" :
        - this form can be seen in the profile page, this form give you ability to change the password and decrypt it.

    changeUser - "/changeUser" :
        - this form will check if the new username was exect in the database or not, if exict it will return error message otherwise it will change the username

    history - "/history" :
        - this page has form will will accept the day you want to see the history of , after submit it will show your achivment


/templates:
    layout.html :
        has header design and its the main page of the web app.

    home.html :
        its the home page of the web app and has to butten, one to login and other to register.

        if you log in the login and register butten will be gone .
    history.html :
        history page will show the last day number and will give u abilite to see your achivement.

        you should be loged in to enter this page

    login.html :
        login page give you the ability to login to the web app.

    register.html :
        give you ability to create new username and password

    profile.html :
        this page give you ability to see your username, change username and password, and show you the day counter.

    MyDocument.html :
         this page is the main page of the web app, here you can enter yout achivment,problem you face, problem you face and solve and the day counter

         also you can found butten called RESTART if you click it, it will delete everythings in the achive table.

/static :
    style.css :
        This one has the design of some part of the home page and other pages

        the other design i use inline way to design the pages

helpers.py :
    this one i get it from week9 problem set "finance".

kunto.db :
    I use the same table i was using in "finance" problem set so there is some tables and columen i didn't used in the project

    DAYs table :
        this table has the days counter.

    achive table :
        this table has the information was given in the MyDocument page.

    users table :
        this table store the information of the users


this is ali and this was CS50