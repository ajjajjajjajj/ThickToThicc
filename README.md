# ThickToThicc

Repository for the ThickToThicc application with Django and Heroku with Raw SQL, using the Heroku PostGres add-on. Django ORM was not used. 

This is our project repository for the AY21/22 Sem 2 module, IT2002 Database Technology and Management. The focus of the project is to build a rudimentary interface for interacting with a database. In the case of our topic, we proposed an application with the motive of connecting gym users, gym trainers and gyms through their common fitness interests and areas, their location and budget, for example. Our site also features a rating system that allows users to rate gyms and trainers. 

The objective of the project is to demonstrate and apply the use of SQL (complex queries, trigger functions, etc) in a simulated environment close to the real world. For example, our search system allows for users to input filter options, and these change the way the SQL query is structured under the hood such that only the rows fitting the indicated filters are retrieved. Another example is the ratings function, which uses trigger functions to automatically update the actual rating of a trainer to the aggregate mean of all of their ratings whenever a new rating is added.
