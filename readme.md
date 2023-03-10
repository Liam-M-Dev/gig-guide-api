# API Webserver Project

## Liam Massey - T2A2

***

### R1 + R2) Identify the problem you are trying to solve by building this app, Why is it a problem that needs solving?

My project is built to create a central location for bands and venues to post upcoming shows and for users to be able to mark themselves as attending the show. I believe this is a solution to the problem where in the local music scene there isn't really a centralized platform that is solely focused on shows. Often you need to follow bands or venues, periodically checking for updates when new shows are happening.  

***

### R3) Why have you chosen this database system. What are the drawbacks compared to others?

***

### R4) Identify and discuss the key functionalities and benefits of an ORM  

***

### R5) Document all endpoints for your API

***

### R6) ERD

![Entity Diagram Relationship](./docs/gig-guide-erd.png)

For this entity relationship diagram provided I have defined four entities and one relationship table. The entities are users, bands, venues and shows and the relationship is between users and shows via the attending table. The user table has a relationship with bands and venues as a user is able to create a venue or a band and associate it with their user identity. The user also has a relationship with the shows entity via the attending table, this allows the user to register there attendance by supplying their users identity and the shows identity.  
Bands and Venues have similar relationships with shows where they are able to create a show and either supply the band ID or the venue ID depending on who creates it.  

***

### R7) Detail any third party services that your app will use

- Flask
- flask-sqlalchemy + SQLAlchemy
- flask-marshmallow + Marshmallow
- flask-bcrypt
- flask-jwt-extender
- Insomnia/postman

***

### R8) Describe your projects models in terms of the relationships they have with each other

The models for this project are:

- User
- Band
- Venue
- Show
- Attending

#### **User**

The User model is the first point of call for this application, as it allows our users to create their own account, create a venue or band account and attend upcoming shows. In the User Model we have 4 attributes and 1 primary key. The primary key is the user_id and is serialized by our database postgresql. For the attributes a user has a first name, last name, email and password, all of these elements are not nullable. The password will also be protected by using password hashing via Bcrypt.  

#### **Band**

The Band model is where users are able to create a band that they currently play in and there is an association between the two with a use of a foreign key that points to the user_id in the users table. The attributes that are related to a band are the band name, the genre of the band(example: punk, pop, metal, electronic) and the state that the band is located in, these are not nullable. A primary key is also supplied as band_id and is serialized by postgresql.  

#### **Venue**

The Venue Model is where users are able to create a venue that hosts the shows, the association between these two is through a foreign key of the user_id. The attributes of a venue are the venue name and location, there is also a primary key for a venue model that is the venue_id and is serialized through postgresql. These attributes are also not nullable.  

#### **Show**

A show model is where bands or venues are able to create a show that is upcoming. They are associated through foreign keys for both band and venue ids. For the Show model its attributes there are the show name, the date and the associated keys. these are also not nullable. A show also has its own unique primary key which is show id and is serialized through postgresql.  

#### **Attending**

Attending model is to represent the relationship between a user and shows. It is made up of a primary key for the attending_id, and 2 foreign keys the user_id and the show_id, which are both not nullable.  

***

### R9) Discuss the database relations to be implemented in your application

The relations that are implemented are as follows:  

- Users has a one to many relationship with bands, this is because one user is able to have many bands under their ID. This is shown through the ERD with the band model having a foreign key that points to a user_id. This is a reality in the real world because being a musician allows you to play for multiple bands with different genres or the same genre.
- Users have a one to many relationship with venues, as one user can own multiple venues. This is shown through the ERD by implementing a user_id as a foreign key inside the venue model that helps point a venue back to a user within the users table. In the real world often multiple venues can be owned by the same person and I was wanting to reflect that within my API.
- Users also have a many to many relationship with shows, that is associated within the Attending table via foreign key within the model. You can see this represented in the ERD with the one to many line connecting users to the attending table. This reflects reality as a person is able to book themselves into multiple shows.  
- Bands have a one to many relationship with the shows. this is represented through the ERD with the one to many connection and a band_id associated within the show model. This allows bands to create multiple shows however a band cannot create the same show at the same venue on the same date. This is reflected in the real world as bands tend to play multiple shows on a night or over a period of time, or they may play the same show at different venues.
- Venues have a one to many relationship with shows that is associated within the show table as a one to many line on the ERD. This points a show to a venue_id via a foreign key. In reality venues often have multiple shows on during the week and on the same night, to help differentiate the shows this allows a connection to which venue is hosting what gig and which bands will be playing that gig.
- Shows has a many to many relationship with users that is associated within the attending table as well. You can see this represented within the ERD. The attending table allows many shows to be associated to many users through the foreign keys within the attending model.

***

### R10) Describe the way tasks are allocated and tracked in your project

For this project I decided to use Trello boards with a kanban style set up of the cards. In each card there is often checklists to check off as I am going through this project, I have set realistic dates to achieve these by that allows for time to make sure everything is running smoothly towards the end of the project.

The initial phase of the setup is done through a few various cards which are, the create virtual environment card, set up postgresql card - setting dates for these as the 2nd of March. My next step is to create the main application file, main.py, creating a config file and connecting that to the main app function. Also have the set up for the .env and .flask-env files. These cards have set dates for the 4th of March to be completed.  

I have created a card for creating the models of my project, each model has checklists to be completed within in them. The checklists include setting up the fields of the model, defining the primary key and defining the relationships that are represented between the models. For the models card I have set the date for completion on the 5th of March.  

Schemas are also defined in the schema card with checklists for each schema to ensure that it is completed and covers what is needed. Inside each checklist I have to implement the fields for each schema, implement the nesting of relationships that is appropriate through marshmallow and its functions such as fields, list etc. This is also set to be completed on the 5th of March.  

Creating CLI commands is my next task to ensure that the connection between the database and the flask app is working as intended. To do this I have set out a checklist to ensure that I create a function to create the database, drop the database and seed the database with information of 5 users, 5 bands, 5 venues, 10 shows and 4 attending. The intention is to have this done by the 6th of March.  

Once CLI commands are finalized within the app, I am going to create my initial setup of controllers. This is tracked via the controllers card, which has a checklist for each individual controller and for the init.py file. Within the init.py file I have a checklist to ensure each controller is added to the registerable controllers, and then implemented into the main app function. Each individual controller has a check list that ensures the blueprints are created and an initial get route to display the information for each table. This will be tracked with the use of Insomnia to ensure that the results are produced correctly. The due date for this is the 7th of March.

The next task is to initialize the routing and implement all the functions and features that I am intending to have related to the databases.  
To begin the process I have a card representing the routing for Users, With a checklist that ticks off the CRUD features, creating a user, reading users, updating users and deleting users, ensuring there is also appropriate authentication and validation and implementing searching functions to allow show the user what venues or bands are connected to their ID. Implementation plan of this is to have it done by the 8th.  
Routing for bands is the next one on the list and follows a similar line of checking the CRUD features, also creating search features to show bands with their upcoming shows, similar genres and states and displaying bands that have connected user IDs.  
Routing for venues is the next card to check off that follows the same principals as before with CRUD features and displaying shows that are upcoming associated with the venue as well as displaying user ids that connect to the venues.  
Routing for Shows again follows similar CRUD principals allowing a venue or band to create, update, read and delete upcoming shows. It also has features to display shows that are connected to one venue or shows that are connected to one band.  
The Attending routing is done through users which gives users the ability to add themselves as attending to a show, delete their attendance to a show and update their attendance to a different show. It also allows displaying of users going to a single show and shows that one user is selected to attend. These routes are all intended to be finalized by the 12th of March.  
Finally the last cards are for the documentation that is intended to finish up by the 17th of March. To have all the coding finished by the 12th is my ideal mission as this allows for testing to ensure everything is being handled appropriately, error handing is completely covered and if any features need editing or adding.  
***

### Software Development Plan

***
