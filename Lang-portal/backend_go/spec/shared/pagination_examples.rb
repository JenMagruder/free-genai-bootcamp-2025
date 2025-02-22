RSpec.shared_examples 'paginated response' do
  it 'has pagination metadata' do
    expect(json_response).to include(
      'current_page',
      'total_pages',
      'total_items',
      'items_per_page'
    )
  end

  it 'has valid pagination values' do
    expect(json_response['current_page']).to be >= 1
    expect(json_response['total_pages']).to be >= 0
    expect(json_response['total_items']).to be >= 0
    expect(json_response['items_per_page']).to be > 0
  end

  it 'has items array' do
    expect(json_response['items']).to be_an(Array)
  end
end
