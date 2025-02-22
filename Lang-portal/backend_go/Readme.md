## Run

```sh
go run cmd/server/main.go
```

## Test Code

When running tests, use test database for the go app:
```sh
DB_PATH=./words.test.db go run cmd/server/main.go
```

Running a test:

```sh
rspec spec/api/words_spec.rb
```

Running all test:

```sh
rspec spec/api/*
```

## Kill if already running

If the port is already in use from running go app prior you can, kill the process:
```sh
lsof -ti:8081 | xargs kill -9
```

### Running mage commands

```sh
go run github.com/magefile/mage@latest testdb
go run github.com/magefile/mage@latest dbinit
go run github.com/magefile/mage@latest seed
```