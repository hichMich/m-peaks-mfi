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

### Improvements
- Add a BD backup with postgis extension
- Add unit testing
- Add migrations