const { Client } = require('@notionhq/client');
require('dotenv').config();

const notion = new Client({ auth: process.env.NOTION_TOKEN });

async function checkDatabaseAccess(databaseId) {
    try {
        console.log(`🔍 Checking access to database: ${databaseId}`);
        
        const response = await notion.databases.retrieve({
            database_id: databaseId
        });
        
        console.log('✅ Database access successful!');
        console.log('📊 Database info:');
        console.log('  Title:', response.title?.[0]?.plain_text || 'Untitled');
        console.log('  Created:', response.created_time);
        console.log('  Properties:', Object.keys(response.properties).join(', '));
        
        return true;
    } catch (error) {
        console.log('❌ Database access failed:');
        console.log('  Error:', error.message);
        if (error.code === 'object_not_found') {
            console.log('  → Database not shared with n8n integration');
            console.log('  → Please share the database with your n8n integration in Notion');
        }
        return false;
    }
}

async function waitForDatabaseAccess(databaseId, maxAttempts = 30) {
    console.log('⏳ Waiting for database to be shared with n8n integration...');
    console.log('📝 Please share your Notion database with the "n8n" integration');
    console.log('');
    
    for (let i = 1; i <= maxAttempts; i++) {
        console.log(`🔄 Attempt ${i}/${maxAttempts}...`);
        
        const hasAccess = await checkDatabaseAccess(databaseId);
        if (hasAccess) {
            console.log('🎉 Database access granted! Ready to create pages!');
            return true;
        }
        
        if (i < maxAttempts) {
            console.log('⏱️  Waiting 5 seconds before next check...');
            await new Promise(resolve => setTimeout(resolve, 5000));
        }
    }
    
    console.log('⏰ Timeout waiting for database access');
    return false;
}

// Run if called directly
if (require.main === module) {
    const databaseId = process.env.NOTION_DATABASE_ID;
    
    if (!databaseId || databaseId === 'your_notion_database_id_here') {
        console.error('❌ Please set NOTION_DATABASE_ID in .env file');
        process.exit(1);
    }
    
    console.log('🎯 AUTOCREATE Notion Database Access Checker');
    console.log('=============================================');
    console.log('');
    
    if (process.argv[2] === 'wait') {
        waitForDatabaseAccess(databaseId)
            .then(success => process.exit(success ? 0 : 1));
    } else {
        checkDatabaseAccess(databaseId)
            .then(success => process.exit(success ? 0 : 1));
    }
}

module.exports = { checkDatabaseAccess, waitForDatabaseAccess };
