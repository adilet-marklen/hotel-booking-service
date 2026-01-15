CREATE TABLE rooms (
  id BIGSERIAL PRIMARY KEY,
  description TEXT NOT NULL,
  price NUMERIC(10,2) NOT NULL CHECK (price > 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE bookings (
  id BIGSERIAL PRIMARY KEY,
  room_id BIGINT NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
  date_start DATE NOT NULL,
  date_end DATE NOT NULL,
  CHECK (date_end >= date_start)
);

CREATE INDEX bookings_room_start_idx ON bookings (room_id, date_start);
