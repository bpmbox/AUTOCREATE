const { Client } = require('@notionhq/client');
require('dotenv').config();

// Demo/test mode - show what the script would do
console.log('🎯 AUTOCREATE Notion Page Creator - Demo Mode');
console.log('===============================================');
console.log('');

// Check environment variables
console.log('📋 Environment Check:');
console.log('NOTION_TOKEN:', process.env.NOTION_TOKEN ? 'SET ✅' : 'NOT SET ❌');
console.log('NOTION_DATABASE_ID:', process.env.NOTION_DATABASE_ID || 'NOT SET');
console.log('');

if (!process.env.NOTION_TOKEN) {
    console.error('❌ NOTION_TOKEN not found in .env file');
    console.error('Please add your Notion integration token to .env file');
    process.exit(1);
}

if (!process.env.NOTION_DATABASE_ID || process.env.NOTION_DATABASE_ID === 'your_notion_database_id_here') {
    console.log('⚠️  NOTION_DATABASE_ID not configured - Running in DEMO mode');
    console.log('');
    console.log('🎨 Sample Page Structure:');
    console.log('');
    
    const samplePageStructure = {
        "cover": {
            "type": "external",
            "external": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
            }
        },
        "icon": {
            "type": "emoji",
            "emoji": "🥬"
        },
        "parent": {
            "type": "database_id",
            "database_id": "YOUR_DATABASE_ID_HERE"
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": "Tuscan kale - Created by AUTOCREATE"
                        }
                    }
                ]
            },
            "Description": {
                "rich_text": [
                    {
                        "text": {
                            "content": "A sample page created by the AUTOCREATE system"
                        }
                    }
                ]
            }
        }
    };
    
    console.log(JSON.stringify(samplePageStructure, null, 2));
    console.log('');
    console.log('🔧 To use this for real:');
    console.log('1. Create a database in Notion');
    console.log('2. Update NOTION_DATABASE_ID in .env file');
    console.log('3. Run: node notion_page_creator.js');
    console.log('');
    console.log('📖 See NOTION_SETUP_GUIDE.md for detailed instructions');
    
    return;
}

// If we have a valid database ID, proceed with the real script
const notion = new Client({ auth: process.env.NOTION_TOKEN });

async function createSamplePage(title = "Tuscan kale - Created by AUTOCREATE", description = "A dark green leafy vegetable - Sample page created by AUTOCREATE system") {
  try {
    console.log('Creating a sample page in Notion...');
    console.log('Using database ID:', process.env.NOTION_DATABASE_ID);
    
    const response = await notion.pages.create({
      "cover": {
          "type": "external",
          "external": {
              "url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
          }
      },
      "icon": {
          "type": "emoji",
          "emoji": "🥬"
      },
      "parent": {
          "type": "database_id",
          "database_id": process.env.NOTION_DATABASE_ID
      },
      "properties": {
          "Name": {
              "title": [
                  {
                      "text": {
                          "content": title
                      }
                  }
              ]
          },
          "Description": {
              "rich_text": [
                  {
                      "text": {
                          "content": description
                      }
                  }
              ]
          },
          "Food group": {
              "select": {
                  "name": "🥬 Vegetable"
              }
          }
      },
      "children": [
          {
              "object": "block",
              "heading_2": {
                  "rich_text": [
                      {
                          "text": {
                              "content": "AUTOCREATE Knowledge Registration"
                          }
                      }
                  ]
              }
          },
          {
              "object": "block",
              "paragraph": {
                  "rich_text": [
                      {
                          "text": {
                              "content": "This is a sample page created by the AUTOCREATE system to demonstrate Notion API integration. The system can automatically register knowledge, create documentation, and manage content in your Notion workspace.",
                              "link": null
                          }
                      }
                  ],
                  "color": "default"
              }
          },
          {
              "object": "block",
              "heading_3": {
                  "rich_text": [
                      {
                          "text": {
                              "content": "System Information"
                          }
                      }
                  ]
              }
          },
          {
              "object": "block",
              "paragraph": {
                  "rich_text": [
                      {
                          "text": {
                              "content": `Created at: ${new Date().toISOString()}\nProject: AUTOCREATE AI System\nEnvironment: ${process.env.NODE_ENV || 'development'}`
                          }
                      }
                  ]
              }
          }
      ]
    });
    
    console.log('✅ Successfully created page!');
    console.log('Page ID:', response.id);
    console.log('Page URL:', response.url);
    console.log('Full response:', JSON.stringify(response, null, 2));
    
    return response;
    
  } catch (error) {
    console.error('❌ Error creating page:', error.message);
    if (error.code === 'validation_error') {
      console.error('Validation error details:', error.body);
    }
    if (error.code === 'object_not_found') {
      console.error('Database not found. Please check your NOTION_DATABASE_ID in .env file');
    }
    throw error;
  }
}

// Run if called directly
if (require.main === module) {
  const action = process.argv[2] || 'sample';
  console.log(`Running action: ${action}`);
  
  createSamplePage()
    .then(() => console.log('Sample script completed successfully'))
    .catch(() => process.exit(1));
}

module.exports = { createSamplePage };
