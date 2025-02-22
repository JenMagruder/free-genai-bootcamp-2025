require_relative '../spec_helper'

RSpec.describe 'Study Sessions API' do
  include ApiHelper

  describe 'GET /study_sessions' do
    let(:response) { HTTParty.get("#{api_url}/study_sessions") }

    it 'returns status 200' do
      expect(response.code).to eq(200)
    end

    it 'returns paginated list of study sessions' do
      body = json_response
      expect(body).to include('items', 'current_page', 'total_pages')
    end
  end

  describe 'POST /study_sessions/:id/words/:word_id/review' do
    context 'with valid ids' do
      let(:response) do
        HTTParty.post(
          "#{api_url}/study_sessions/1/words/1/review",
          query: { correct: true }
        )
      end

      it 'returns status 200' do
        expect(response.code).to eq(200)
      end
    end

    context 'with invalid ids' do
      let(:response) do
        HTTParty.post(
          "#{api_url}/study_sessions/999/words/999/review",
          query: { correct: true }
        )
      end

      it 'returns status 404' do
        expect(response.code).to eq(404)
      end
    end
  end
end
