require_relative '../spec_helper'

RSpec.describe 'Study Activities API' do
  include ApiHelper

  describe 'GET /study_activities/:id' do
    context 'with valid id' do
      let(:response) { HTTParty.get("#{api_url}/study_activities/1") }

      it 'returns status 200' do
        expect(response.code).to eq(200)
      end

      it 'returns activity with correct properties' do
        activity = json_response
        expect(activity).to include('id', 'name')
      end
    end

    context 'with invalid id' do
      let(:response) { HTTParty.get("#{api_url}/study_activities/999") }

      it 'returns status 404' do
        expect(response.code).to eq(404)
      end
    end
  end

  describe 'GET /study_activities/:id/study_sessions' do
    context 'with valid id' do
      let(:response) { HTTParty.get("#{api_url}/study_activities/1/study_sessions") }

      it 'returns status 200' do
        expect(response.code).to eq(200)
      end

      it 'returns paginated list of study sessions' do
        body = json_response
        expect(body).to include('items', 'current_page', 'total_pages')
      end

      it 'has sessions with correct properties' do
        body = json_response
        if body['items'].any?
          session = body['items'].first
          expect(session).to include('id', 'created_at', 'group_id', 'study_activity_id')
        end
      end
    end
  end

  describe 'POST /study_activities' do
    let(:response) do
      HTTParty.post(
        "#{api_url}/study_activities",
        body: {
          group_id: 1,
          study_activity_id: 1
        }.to_json,
        headers: { 'Content-Type' => 'application/json' }
      )
    end

    it 'returns status 200' do
      expect(response.code).to eq(200)
    end

    it 'returns created study session' do
      session = json_response
      expect(session).to include('id', 'created_at', 'group_id', 'study_activity_id')
    end
  end
end
