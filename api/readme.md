## Flask Lab 2

### External libraries
We will be using Flask, flask_httpauth for this.

In case you do not have them: 
```cmd
pip install Flask
pip install flask_httpauth
```

### Code Structure

#### Top level
- app.py: Applications entrypoint. Used to start the webserver. Here we register our blueprints
- base_logger.py: Configuration of the logger to be used across the application
- xx_controller.py: The routes, the logic and the auth mechanism for our app.
- xx_service.py: The processing that needs to be made to our data.

#### Local Run
In the top level of the directory of task_app fire up a terminal and execute:
```cmd
python3 app.py
```
Note that `python3` may not be needed in your setup, and you may need `python` or `python3.8` whatever you have in your 
operating system's PATH

For all the get requests you can go to any browser and make type the endpoint in URL.
E.g, `http://127.0.0.1:5000/todo/api/v1.0/tasks`

For the rest of the requests you need to use an HTTP client (Postman for instance).

#### Postman Collection
You can import the collection (tasks.postman_collection.json)
directly in Postman where some sample RQs exist already.

#### Authorization
If you check the code (model_controller) you will see that employee routes are protected with Basic Auth.
In Postman to add the corresponding username and password go to Authorization tab select Basic Auth from the type dropdown and add the username and password (python and my_python respectively or johndoe with password johndoe).
