require_relative '../spec_helper'

RSpec.describe 'Groups API' do
  describe 'GET /groups' do
    let(:response) { HTTParty.get("#{api_url}/groups") }

    it 'returns status 200' do
      expect(response.code).to eq(200)
    end

    it 'returns paginated list of groups' do
      body = json_response
      expect(body).to include('items', 'pagination')
    end

    it 'has correct pagination structure' do
      body = json_response
      expect(body['pagination']).to include(
        'current_page',
        'total_pages',
        'total_items',
        'items_per_page'
      )
    end

    it 'has 100 items per page' do
      body = json_response
      expect(body['pagination']['items_per_page']).to eq(100)
    end

    it 'has groups with correct properties' do
      body = json_response
      if body['items'].any?
        group = body['items'].first
        expect(group).to include(
          'id',
          'name',
          'stats'
        )
        expect(group['stats']).to include('total_word_count')
      end
    end

    it 'has correct value types' do
      body = json_response
      if body['items'].any?
        group = body['items'].first
        expect(group['id']).to be_a(Integer)
        expect(group['name']).to be_a(String)
        expect(group['stats']['total_word_count']).to be_a(Integer)
      end
    end
  end

  describe 'GET /groups/:id/words' do
    context 'with valid id' do
      let(:response) { HTTParty.get("#{api_url}/groups/1/words") }

      it 'returns status 200' do
        expect(response.code).to eq(200)
      end

      it 'returns paginated list of words' do
        body = json_response
        expect(body).to include('items', 'pagination')
      end

      it 'has correct pagination structure' do
        body = json_response
        expect(body['pagination']).to include(
          'current_page',
          'total_pages',
          'total_items',
          'items_per_page'
        )
      end

      it 'has 100 items per page' do
        body = json_response
        expect(body['pagination']['items_per_page']).to eq(100)
      end

      it 'has words with correct properties' do
        body = json_response
        if body['items'].any?
          word = body['items'].first
          expect(word).to include(
            'japanese',
            'romaji',
            'english',
            'correct_count',
            'wrong_count'
          )
        end
      end

      it 'has correct value types' do
        body = json_response
        if body['items'].any?
          word = body['items'].first
          expect(word['japanese']).to be_a(String)
          expect(word['romaji']).to be_a(String)
          expect(word['english']).to be_a(String)
          expect(word['correct_count']).to be_a(Integer)
          expect(word['wrong_count']).to be_a(Integer)
        end
      end
    end

    context 'with invalid id' do
      let(:response) { HTTParty.get("#{api_url}/groups/999/words") }

      it 'returns status 404' do
        expect(response.code).to eq(404)
      end
    end
  end
end
