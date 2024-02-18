# Welcome to Mountain Peaks API
This is a public repo, to use this API, you must befor of all do:
```
    git clone https://github.com/hichMich/m-peaks-mfi.git
```

### How to launch it
Navigate to the directory containing the docker-compose.yml file and execute the following commands.
- to build all images and up the entire stack:
```
    docker-compose up --build
```
- to down the entire stack:
```
    docker-compose down -v --remove-orphans
```

### How to use it
##### Examples of bbox
You can pass this parameters in the endpoint to test get bbox
bbox = (27.9, 86.8, 28.1, 87.1)


### Improvements
- Add a BD backup with postgis extension
- Add unit testing
- Add migrations

