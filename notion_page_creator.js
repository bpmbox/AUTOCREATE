const { Client } = require('@notionhq/client');
require('dotenv').config();

// Check environment variables
if (!process.env.NOTION_TOKEN) {
    console.error('❌ NOTION_TOKEN not found in .env file');
    console.error('Please add your Notion integration token to .env file');
    process.exit(1);
}

if (!process.env.NOTION_DATABASE_ID || process.env.NOTION_DATABASE_ID === 'your_notion_database_id_here') {
    console.error('❌ NOTION_DATABASE_ID not configured properly in .env file');
    console.error('Current value:', process.env.NOTION_DATABASE_ID);
    console.error('Please add your actual Notion database ID to .env file');
    console.error('See NOTION_SETUP_GUIDE.md for setup instructions');
    process.exit(1);
}

const notion = new Client({ auth: process.env.NOTION_TOKEN });

// ...existing code...