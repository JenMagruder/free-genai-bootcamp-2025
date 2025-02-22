-- Insert basic groups
INSERT INTO groups (name) VALUES
    ('Basic Greetings'),
    ('Numbers'),
    ('Colors'),
    ('Family Members');

-- Insert some basic Japanese words
INSERT INTO words (japanese, romaji, english, parts) VALUES
    ('こんにちは', 'konnichiwa', 'hello', '{"type": "greeting", "formality": "neutral"}'),
    ('さようなら', 'sayounara', 'goodbye', '{"type": "greeting", "formality": "formal"}'),
    ('おはよう', 'ohayou', 'good morning', '{"type": "greeting", "formality": "informal"}'),
    ('一', 'ichi', 'one', '{"type": "number", "category": "cardinal"}'),
    ('二', 'ni', 'two', '{"type": "number", "category": "cardinal"}'),
    ('三', 'san', 'three', '{"type": "number", "category": "cardinal"}'),
    ('赤', 'aka', 'red', '{"type": "color", "category": "basic"}'),
    ('青', 'ao', 'blue', '{"type": "color", "category": "basic"}'),
    ('黄色', 'kiiro', 'yellow', '{"type": "color", "category": "basic"}'),
    ('お父さん', 'otousan', 'father', '{"type": "family", "formality": "polite"}'),
    ('お母さん', 'okaasan', 'mother', '{"type": "family", "formality": "polite"}'),
    ('兄', 'ani', 'older brother', '{"type": "family", "formality": "plain"}');

-- Link words to groups
INSERT INTO words_groups (word_id, group_id) 
SELECT w.id, g.id 
FROM words w, groups g 
WHERE 
    (w.japanese IN ('こんにちは', 'さようなら', 'おはよう') AND g.name = 'Basic Greetings')
    OR (w.japanese IN ('一', '二', '三') AND g.name = 'Numbers')
    OR (w.japanese IN ('赤', '青', '黄色') AND g.name = 'Colors')
    OR (w.japanese IN ('お父さん', 'お母さん', '兄') AND g.name = 'Family Members');

-- Insert a study activity
INSERT INTO study_activities (id, name, thumbnail_url, description) VALUES
    (1, 'Vocabulary Quiz', 'https://example.com/vocab-quiz.jpg', 'Practice your vocabulary with flashcards'),
    (2, 'Writing Practice', 'https://example.com/writing.jpg', 'Practice writing Japanese characters'),
    (3, 'Listening Exercise', 'https://example.com/listening.jpg', 'Improve your listening comprehension');

-- Create some sample study sessions
INSERT INTO study_sessions (group_id, study_activity_id) 
SELECT g.id, 1
FROM groups g
WHERE g.name IN ('Basic Greetings', 'Numbers')
LIMIT 2;

-- Add some word review items
INSERT INTO word_review_items (word_id, study_session_id, correct)
SELECT w.id, s.id, (RANDOM() > 0.5)
FROM words w
CROSS JOIN study_sessions s
WHERE w.japanese IN ('こんにちは', 'さようなら', '一', '二')
LIMIT 8;
