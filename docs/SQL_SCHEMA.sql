CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  username VARCHAR(150) UNIQUE NOT NULL,
  email VARCHAR(254) UNIQUE NOT NULL,
  password VARCHAR(128) NOT NULL,
  is_email_verified BOOLEAN NOT NULL DEFAULT FALSE,
  avatar VARCHAR(100),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  is_staff BOOLEAN NOT NULL DEFAULT FALSE,
  is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
  date_joined TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE profiles (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  display_name VARCHAR(120) NOT NULL DEFAULT '',
  bio VARCHAR(240) NOT NULL DEFAULT '',
  timezone VARCHAR(64) NOT NULL DEFAULT 'UTC',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE chats (
  id BIGSERIAL PRIMARY KEY,
  type VARCHAR(16) NOT NULL CHECK (type IN ('direct', 'group')),
  title VARCHAR(160) NOT NULL DEFAULT '',
  created_by_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE chat_members (
  id BIGSERIAL PRIMARY KEY,
  chat_id BIGINT NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role VARCHAR(16) NOT NULL DEFAULT 'member',
  joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  muted_until TIMESTAMPTZ,
  CONSTRAINT unique_chat_member UNIQUE (chat_id, user_id)
);

CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  chat_id BIGINT NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
  sender_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  body TEXT NOT NULL DEFAULT '',
  status VARCHAR(16) NOT NULL DEFAULT 'sent',
  reply_to_id BIGINT REFERENCES messages(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  edited_at TIMESTAMPTZ,
  deleted_at TIMESTAMPTZ
);

CREATE TABLE read_receipts (
  id BIGSERIAL PRIMARY KEY,
  message_id BIGINT NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  read_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT unique_message_reader UNIQUE (message_id, user_id)
);

CREATE TABLE notifications (
  id BIGSERIAL PRIMARY KEY,
  recipient_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  actor_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
  type VARCHAR(24) NOT NULL,
  title VARCHAR(160) NOT NULL,
  body VARCHAR(500) NOT NULL DEFAULT '',
  data JSONB NOT NULL DEFAULT '{}',
  read_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_chat_created ON messages(chat_id, created_at DESC);
CREATE INDEX idx_chat_members_user_chat ON chat_members(user_id, chat_id);
CREATE INDEX idx_notifications_recipient_unread ON notifications(recipient_id, read_at, created_at DESC);
CREATE INDEX idx_chats_type_updated ON chats(type, updated_at DESC);
