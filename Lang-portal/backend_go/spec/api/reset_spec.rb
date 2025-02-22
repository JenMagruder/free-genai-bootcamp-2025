require_relative '../spec_helper'

# ignore for now.
# it would mess up the specs because of the database cleanup that happens in full_reset

#RSpec.describe 'Reset API' do
#  include ApiHelper
#
#  describe 'POST /reset_history' do
#    let(:response) { HTTParty.post("#{api_url}/reset_history") }
#
#    it 'returns status 200' do
#      expect(response.code).to eq(200)
#    end
#
#    it 'actually resets study history' do
#      # First create some study history
#      HTTParty.post(
#        "#{api_url}/study_sessions/1/words/1/review",
#        query: { correct: true }
#      )
#
#      # Then reset it
#      reset_response = HTTParty.post("#{api_url}/reset_history")
#      expect(reset_response.code).to eq(200)
#
#      # Check that study history is cleared
#      stats = HTTParty.get("#{api_url}/dashboard/quick-stats")
#      stats_body = JSON.parse(stats.body)
#      expect(stats_body['words_learned']).to eq(0)
#      expect(stats_body['words_in_progress']).to eq(0)
#    end
#  end
#
#  describe 'POST /full_reset' do
#    let(:response) { HTTParty.post("#{api_url}/full_reset") }
#
#    it 'returns status 200' do
#      expect(response.code).to eq(200)
#    end
#
#    it 'resets entire database' do
#      # First create some data
#      HTTParty.post(
#        "#{api_url}/study_activities",
#        body: {
#          group_id: 1,
#          study_activity_id: 1
#        }.to_json,
#        headers: { 'Content-Type' => 'application/json' }
#      )
#
#      # Then do full reset
#      reset_response = HTTParty.post("#{api_url}/full_reset")
#      expect(reset_response.code).to eq(200)
#
#      # Check that data is reset
#      words = HTTParty.get("#{api_url}/words")
#      words_body = JSON.parse(words.body)
#      expect(words_body['pagination']['total_items']).to eq(3) # Only seed data should remain
#    end
#  end
#end
#