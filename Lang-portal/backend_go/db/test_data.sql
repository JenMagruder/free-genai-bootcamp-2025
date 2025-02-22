-- Insert test words with specific IDs
INSERT INTO words (id, japanese, romaji, english) VALUES
(1, '犬', 'inu', 'dog'),
(2, '猫', 'neko', 'cat'),
(3, '鳥', 'tori', 'bird');

-- Insert test groups with specific IDs
INSERT INTO groups (id, name) VALUES
(1, 'Animals'),
(2, 'Basic Words');

-- Insert test word-group relationships
INSERT INTO words_groups (word_id, group_id) VALUES
(1, 1),
(2, 1),
(3, 1);

-- Insert test study activities
INSERT INTO study_activities (id, name, thumbnail_url, description) VALUES
(1, 'Flashcards', 'https://example.com/flashcards.png', 'Practice with flashcards'),
(2, 'Multiple Choice', 'https://example.com/quiz.png', 'Test your knowledge with multiple choice questions');

-- Insert test study sessions
INSERT INTO study_sessions (id, group_id, created_at, study_activity_id) VALUES
(1, 1, datetime('now', '-1 day'), 1),
(2, 1, datetime('now'), 1);

-- Insert test word review items
INSERT INTO word_review_items (word_id, study_session_id, correct, created_at) VALUES
(1, 1, true, datetime('now', '-1 day')),
(2, 1, false, datetime('now', '-1 day')),
(3, 2, true, datetime('now'));
