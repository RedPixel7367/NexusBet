import { createPool } from '@vercel/postgres';
import bcrypt from 'bcryptjs';

const pool = createPool({
    connectionString: process.env.STORAGE_POSTGRES_URL
});

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { email, password } = req.body;
        if (!email || !password) {
            return res.status(400).json({ error: 'Email and password are required' });
        }

        const { rows } = await pool.sql`SELECT password_hash FROM users WHERE email = ${email}`;
        if (rows.length === 0) {
            return res.status(400).json({ error: 'User not found' });
        }

        const match = await bcrypt.compare(password, rows[0].password_hash);
        if (!match) {
            return res.status(400).json({ error: 'Wrong password' });
        }

        return res.status(200).json({ message: 'Login successful' });
    } catch (error) {
        console.error('Login error:', error);
        return res.status(500).json({ error: 'Database error. Make sure Vercel Postgres is connected.' });
    }
}
