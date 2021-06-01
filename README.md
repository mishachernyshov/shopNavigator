# Shop navigator
Shop navigator is a web-application that allow clients to manage shops, 
collection of products that are available in the system and determine 
what products should be available in a shop, how much do they cost and 
how many units of the product are available. So, users can perform CRUD
operations with products, shops and shop products. Also, the application
calculates aggregated information about shops to have an ability to 
compare them according to different indicators. User can filter shop 
products list by price range or find products that have specified price.

## Application building and starting
The application is installable thanks to the setup.py file inside the 
project root directory. So, the user should activate virtual environment 
in this directory, executing the `source virtualenv/bin/activate` command
in the terminal, make sure all libraries are installed by running 
`pip install -r requirements.txt`, after that install the application, 
executing `pip install -e .` there. It allows you to start it using 
development server by running `flask run` command.

For running the server using Gunicorn, after libraries installation, you
can run `gunicorn -b 127.0.0.1:5000 shop_navigator_app:app`, but you also
can change the host address and port. 

To not work with virtual environment, you can run gunicorn using 
`shop_navigator.service` file, that is inside the project root directory,
but it must be moved into the `/etc/systemd/system/` directory. After that,
you can start the project from any directory, typing into the terminal 
`sudo systemctl start shop_navigator` and 
`sudo systemctl enable shop_navigator`. To check the running status you can
type `sudo systemctl status`.

The application will be available by http://127.0.0.1:5000/ URI.