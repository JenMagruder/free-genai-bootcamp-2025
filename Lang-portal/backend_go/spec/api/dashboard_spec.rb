require_relative '../spec_helper.rb'

RSpec.describe 'Dashboard API' do
  describe 'GET /dashboard/quick-stats' do
    let(:response) { HTTParty.get("#{api_url}/dashboard/quick-stats") }

    it 'returns status 200' do
      expect(response.code).to eq(200)
    end

    it 'returns stats with correct properties' do
      stats = json_response
      expect(stats).to include(
        'success_rate',
        'total_study_sessions',
        'total_active_groups',
        'study_streak_days'
      )
    end

    it 'has correct value types' do
      stats = json_response
      expect(stats['success_rate']).to be_a(Float)
      expect(stats['total_study_sessions']).to be_a(Integer)
      expect(stats['total_active_groups']).to be_a(Integer)
      expect(stats['study_streak_days']).to be_a(Integer)
    end
  end

  describe 'GET /dashboard/study_progress' do
    let(:response) { HTTParty.get("#{api_url}/dashboard/study_progress") }

    it 'returns status 200' do
      expect(response.code).to eq(200)
    end

    it 'returns study progress data' do
      progress = json_response
      expect(progress).to include(
        'total_words_studied',
        'total_available_words'
      )
    end

    it 'has numeric values' do
      progress = json_response
      expect(progress['total_words_studied']).to be_a(Integer)
      expect(progress['total_available_words']).to be_a(Integer)
    end
  end

  describe 'GET /dashboard/last_study_session' do
    let(:response) { HTTParty.get("#{api_url}/dashboard/last_study_session") }

    context 'when no study sessions exist' do
      it 'returns status 404' do
        expect(response.code).to eq(404)
      end

      it 'returns error message' do
        error = json_response
        expect(error).to include('error')
      end
    end

    context 'when study sessions exist' do
      before do
        # Reset database to ensure test data exists
        HTTParty.post("#{api_url}/full_reset")
        
        # Create a study session first
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
        response = HTTParty.get("#{api_url}/dashboard/last_study_session")
        expect(response.code).to eq(200)
      end

      it 'returns session with correct properties' do
        response = HTTParty.get("#{api_url}/dashboard/last_study_session")
        session = JSON.parse(response.body)
        expect(session).to include(
          'id',
          'group_id',
          'created_at',
          'study_activity_id',
          'group_name'
        )
      end

      it 'has correct value types' do
        response = HTTParty.get("#{api_url}/dashboard/last_study_session")
        session = JSON.parse(response.body)
        expect(session['id']).to be_a(Integer)
        expect(session['group_id']).to be_a(Integer)
        expect(session['created_at']).to match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-\d{2}:\d{2}$/)
        expect(session['study_activity_id']).to be_a(Integer)
        expect(session['group_name']).to be_a(String)
      end
    end
  end
end
