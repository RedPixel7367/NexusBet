import { createPool } from '@vercel/postgres';

const pool = createPool({
    connectionString: process.env.STORAGE_POSTGRES_URL
});

export default async function handler(req, res) {
    try {
        await pool.sql`
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        `;
        return res.status(200).json({ message: 'Users table initialized successfully!' });
    } catch (error) {
        console.error('Init error:', error);
        return res.status(500).json({ error: 'Failed to initialize database. Make sure Vercel Postgres is connected.' });
    }
}
