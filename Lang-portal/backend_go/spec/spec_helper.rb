require 'rspec'
require 'httparty'
require 'json'

# Helper module for API testing
module ApiHelper
  def api_url
    'http://localhost:8081/api'
  end

  def json_response
    JSON.parse(response.body)
  end
end

RSpec.configure do |config|
  config.expect_with :rspec do |expectations|
    expectations.include_chain_clauses_in_custom_matcher_descriptions = true
  end

  config.mock_with :rspec do |mocks|
    mocks.verify_partial_doubles = true
  end

  config.shared_context_metadata_behavior = :apply_to_host_groups

  # Include helper modules
  config.include ApiHelper

  # Initialize test database before running tests
  config.before(:suite) do
    # Initialize test database
    system('mage testdb')
    
    # Start the server with test database
    ENV['DB_PATH'] = './words.test.db'
    system('go run cmd/server/main.go &')
    sleep 2 # Wait for server to start
  end

  # Stop the server after tests
  config.after(:suite) do
    system('pkill -f "go run cmd/server/main.go"')
  end
end
