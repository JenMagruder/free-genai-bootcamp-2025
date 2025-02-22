#!/bin/bash

# Set the test database path
TEST_DB_PATH="./words.test.db"

# Remove existing test database if it exists
rm -f "$TEST_DB_PATH"

# Create new test database and apply schema
sqlite3 "$TEST_DB_PATH" < ./db/migrations/001_initial_schema.sql

# Insert test data
sqlite3 "$TEST_DB_PATH" < ./db/test_data.sql
