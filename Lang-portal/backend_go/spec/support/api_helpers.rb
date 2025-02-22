module ApiHelpers
  def create_study_session
    response = HTTParty.post(
      "#{api_url}/study_activities",
      body: {
        group_id: 1,
        study_activity_id: 1
      }.to_json,
      headers: { 'Content-Type' => 'application/json' }
    )
    JSON.parse(response.body)
  end

  def review_word(session_id, word_id, correct)
    HTTParty.post(
      "#{api_url}/study_sessions/#{session_id}/words/#{word_id}/review",
      query: { correct: correct }
    )
  end

  def get_stats
    response = HTTParty.get("#{api_url}/dashboard/quick-stats")
    JSON.parse(response.body)
  end

  def reset_database
    HTTParty.post("#{api_url}/full_reset")
  end
end
