## cornershop-backend-test

### Running the development environment

* `make up`
* `dev up`

##### Creating superuser for login (Necessary for creating and administrating menus)

* `dev createuser`

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`

### Hostnames for accessing the service directly

* Local: http://127.0.0.1:8000

### URLs

- http://hostname/menu/ : List of all existing menus
- http://hostname/menu/xxxxxxx-xxxxxx-xxxxx/ : Menu form to send responses
- http://hostname/menu/xxxxxxx-xxxxxx-xxxxx/detail/ : Menu detail with list of responses
- http://hostname/login/ : Login page

### API Endpoints

- [GET] http://hostname/menu-api/ : Lists menus
- [POST] http://hostname/menu-api/ : Creates new menu
- [GET] http://hostname/menu-api/xxxxxxx-xxxxxx-xxxxx/ : Retrieves menu info and responses
- [PUT] http://hostname/menu-api/xxxxxxx-xxxxxx-xxxxx/ : Updates menu info
- [DELETE] http://hostname/menu-api/xxxxxxx-xxxxxx-xxxxx/ : Deletes menu
- [GET] http://hostname/menu-api/xxxxxxx-xxxxxx-xxxxx/form/ : Retrieves menu with available options
- [POST] http://hostname/menu-api/xxxxxxx-xxxxxx-xxxxx/respond/ : Saves employee's menu choice
- [POST] http://hostname/menu-api/xxxxxxx-xxxxxx-xxxxx/reminder/ : Sends Slack reminder to employees
- [POST] http://hostname/login/auth/ : Checks login credentials and generates auth token

### Enviroment variables for Slack

In order to send a Slack reminder you need to create an .env file in the cornershop-backend-test folder with the SLACK_TOKEN and SLACK_CHANNEL variables. The SLACK_TOKEN must be generated in the Slack app as shown in https://api.slack.com/authentication/basics#installing
and the SLACK_CHANNEL is the name of the channel in which the reminder will be sent. Example:

```
SLACK_TOKEN="xoxb-XXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXX"
SLACK_CHANNEL=chilean-employees
```

Remember that you have to add the Slack app to the channel.

### About building local environment with Linux systems

If you bring up the local environment in a linux system, maybe you can get some problems about users permissions when working with Docker.
So we give you a little procedure to avoid problems with users permissions structure in Linux.:

1- Delete containers

```
# or docker rm -f $(docker ps -aq) if you don't use docker beyond the test
make down
```

2- Give permissions to your system users to use Docker

```
## Where ${USER} is your current user
sudo usermod -aG docker ${USER}
```

3- Confirm current user is in docker group

```
## If you don't see docker in the list, then you possibly need to log off and log in again in your computer.
id -nG
```


4-  Get the current user id

```
## Commonly your user id number is near to 1000
id -u
```

5- Replace user id in Dockerfiles by your current user id

Edit `.docker/Dockerfile_base` and replace 1337 by your user id.

6- Rebuild the local environment 

```
make rebuild
make up
```