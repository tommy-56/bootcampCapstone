use db;

CREATE TABLE Logs (
    id SERIAL PRIMARY KEY,
    _id VARCHAR(100) NOT NULL, -- Assuming ObjectId as a 24-character hex string
    TimestampServer TIME NOT NULL,
    LogLevel VARCHAR(50) NOT NULL,
    Source VARCHAR(255) NOT NULL,
    Message TEXT NOT NULL
);