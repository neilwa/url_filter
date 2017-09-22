Simple URL filter

### Installation instructions ###

* Build images 
``` docker-compose build ```
* Launch docker instances
``` docker-compose up -d ```
* This will launch 2 docker containers, one for the app instance and one for the redis instance
* Connect to the app container on port 8080 ```http://localhost:8080```
### Usage ###

**Check URL**

* To check a url, send a GET request in the format ```/urlinfo/1/server:port/query```
* The response will be in json format and will contain the category, whether access to the url should be allowed or denied, and the timestamp of the last update. 
* A proxy may decide based on the response to allow or deny access to a site, depending on the category and the timestamp of the last update.

**Add URL**

* To add or update a url, send a POST request to ```/urladd/1``` with json formatted data as per this example```{"url":"url", "category":"category", "result":"allow|deny"}'```
* If the url already exists in the database, the result will be updated. Otherwise the url will be added to the database.

### Reponse format ###
* If url is in the database
```{"category": category, "timestamp": time, "result": result}```
where time is the time the url was last updated in the database and result is 'allow' or 'deny'

* If url is not in the database
```{"category": "unknown", "timestamp": time, "result": "unknown"}```
where time is the time that the request was made
