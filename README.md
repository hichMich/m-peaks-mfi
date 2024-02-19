# Welcome to Mountain Peaks API
This API is for public use, you can simply clone the project without any permission.
```
    git clone https://github.com/hichMich/m-peaks-mfi.git
```

### How to launch it
Navigate to the directory containing the docker-compose.yml file and execute the following commands:
- Build all images and up the entire stack:
```
    docker-compose up --build
```
- Down the entire stack:
```
    docker-compose down -v --remove-orphans
```

### How to use it
##### Discover the API
Open your preferred browser and visit http://localhost:5001/docs to explore all available endpoints in the Swagger page
##### Initialize data
In order to initialize some data in the db, you can simply use this endpoint: /mountain_peaks/init

##### Example of bbox
Test the mountain peak retrieval by bounding box using the following endpoint:
/mountain_peak/bbox/{xmin}/{ymin}/{xmax}/{ymax}
Replace {xmin}, {ymin}, {xmax}, and {ymax} with this latitude and longitude values

```
    xmin = 86.8
    ymin = 27.9
    xmax = 87.0
    ymax = 28.1
```

### Troubleshootings
Launching the entire stack simultaneously may introduce transient connection issues due to PostgreSQL's service startup time. While the API service initiates rapidly, it could attempt to connect to the database before it's available, resulting in a "Connection refused" error.
```
    psql: error: connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
    Is the server running on that host and accepting TCP/IP connections?
```
To mitigate this, our run.sh script incorporates a brief sleep period specifically to facilitate a successful connection attempt after PostgreSQL has fully launched.

### Improvements
- Add a specific service to backup the db.
- Use alembic to manage migrations.
- Add unit testing.
- Setup quality linters to ensure quality of the delivery for example:
  - flake8: code linter
  - black: code formatter
  - bandit: security problems
  - coverage: test report
  - xenon: code complexity linter
- Add CI/CD process with Github actions or gitlab-ci. 