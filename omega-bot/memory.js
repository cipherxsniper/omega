import sqlite3 from "sqlite3";

const db = new sqlite3.Database("./data/omega.db");

// Create table if not exists
db.run(`
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userId TEXT,
  role TEXT,
  message TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
`);

export function saveMessage(userId, role, message) {
  db.run(
    "INSERT INTO messages (userId, role, message) VALUES (?, ?, ?)",
    [userId, role, message]
  );
}

export function getRecentMessages(userId, limit = 10) {
  return new Promise((resolve) => {
    db.all(
      `SELECT role, message FROM messages 
       WHERE userId = ? 
       ORDER BY id DESC 
       LIMIT ?`,
      [userId, limit],
      (err, rows) => {
        if (err) resolve([]);
        else resolve(rows.reverse());
      }
    );
  });
}

export function getUserStats(userId) {
  return new Promise((resolve) => {
    db.get(
      `SELECT COUNT(*) as count FROM messages WHERE userId = ?`,
      [userId],
      (err, row) => {
        if (err) resolve({ count: 0 });
        else resolve(row);
      }
    );
  });
}
