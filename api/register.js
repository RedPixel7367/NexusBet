import { sql } from '@vercel/postgres';
import bcrypt from 'bcryptjs';

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { email, password } = req.body;
        if (!email || !password) {
            return res.status(400).json({ error: 'Email and password are required' });
        }

        // Check if user already exists
        const { rowCount } = await sql`SELECT 1 FROM users WHERE email = ${email}`;
        if (rowCount > 0) {
            return res.status(400).json({ error: 'Email already in use' });
        }

        // Hash password and insert
        const hash = await bcrypt.hash(password, 10);
        await sql`INSERT INTO users (email, password_hash) VALUES (${email}, ${hash})`;

        return res.status(200).json({ message: 'User registered successfully' });
    } catch (error) {
        console.error('Registration error:', error);
        return res.status(500).json({ error: 'Database error. Make sure Vercel Postgres is connected.' });
    }
}
