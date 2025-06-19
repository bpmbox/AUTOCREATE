const { Client } = require('@notionhq/client');
require('dotenv').config();

const notion = new Client({ auth: process.env.NOTION_TOKEN });

async function createPageInHOMEDatabase() {
  try {
    console.log('🏠 Creating page in HOME database...');
    console.log('Database ID:', process.env.NOTION_DATABASE_ID);
    
    const response = await notion.pages.create({
      "cover": {
          "type": "external",
          "external": {
              "url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
          }
      },
      "icon": {
          "type": "emoji",
          "emoji": "🤖"
      },
      "parent": {
          "type": "database_id",
          "database_id": process.env.NOTION_DATABASE_ID
      },
      "properties": {
          "Question 1": {
              "title": [
                  {
                      "text": {
                          "content": "AUTOCREATE AI System - First Success Page! 🎉"
                      }
                  }
              ]
          },
          "Question 2": {
              "multi_select": [
                  {
                      "name": "AUTOCREATE"
                  },
                  {
                      "name": "AI Integration"
                  },
                  {
                      "name": "Success"
                  }
              ]
          },
          "Respondent": {
              "rich_text": [
                  {
                      "text": {
                          "content": "AUTOCREATE AI System"
                      }
                  }
              ]
          },
          "Submission time": {
              "rich_text": [
                  {
                      "text": {
                          "content": new Date().toISOString()
                      }
                  }
              ]
          }
      },
      "children": [
          {
              "object": "block",
              "heading_1": {
                  "rich_text": [
                      {
                          "text": {
                              "content": "🎉 AUTOCREATE Success!"
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
                              "content": "This is the first page successfully created by the AUTOCREATE system in your Notion workspace! The integration is now fully functional and ready for automation.",
                              "link": null
                          }
                      }
                  ],
                  "color": "default"
              }
          },
          {
              "object": "block",
              "heading_2": {
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
              "bulleted_list_item": {
                  "rich_text": [
                      {
                          "text": {
                              "content": "✅ Notion API Integration: Active"
                          }
                      }
                  ]
              }
          },
          {
              "object": "block",
              "bulleted_list_item": {
                  "rich_text": [
                      {
                          "text": {
                              "content": "✅ Chrome Extension: Ready"
                          }
                      }
                  ]
              }
          },
          {
              "object": "block",
              "bulleted_list_item": {
                  "rich_text": [
                      {
                          "text": {
                              "content": "✅ Knowledge Management: Functional"
                          }
                      }
                  ]
              }
          },
          {
              "object": "block",
              "heading_3": {
                  "rich_text": [
                      {
                          "text": {
                              "content": "Next Steps"
                          }
                      }
                  ]
              }
          },
          {
              "object": "block",
              "numbered_list_item": {
                  "rich_text": [
                      {
                          "text": {
                              "content": "Use Chrome Extension automation features"
                          }
                      }
                  ]
              }
          },
          {
              "object": "block",
              "numbered_list_item": {
                  "rich_text": [
                      {
                          "text": {
                              "content": "Configure XPath settings for specific sites"
                          }
                      }
                  ]
              }
          },
          {
              "object": "block",
              "numbered_list_item": {
                  "rich_text": [
                      {
                          "text": {
                              "content": "Create more knowledge pages automatically"
                          }
                      }
                  ]
              }
          },
          {
              "object": "block",
              "divider": {}
          },
          {
              "object": "block",
              "paragraph": {
                  "rich_text": [
                      {
                          "text": {
                              "content": `Created at: ${new Date().toLocaleString()}\nProject: AUTOCREATE AI System\nIntegration: n8n\nDatabase: HOME`
                          }
                      }
                  ],
                  "color": "gray"
              }
          }
      ]
    });
    
    console.log('🎉 SUCCESS! Page created successfully!');
    console.log('📄 Page ID:', response.id);
    console.log('🔗 Page URL:', response.url);
    console.log('📊 Database used: HOME');
    console.log('');
    console.log('✨ Your AUTOCREATE Notion integration is now LIVE! ✨');
    
    return response;
    
  } catch (error) {
    console.error('❌ Error creating page:', error.message);
    if (error.code === 'validation_error') {
      console.error('Validation error details:', JSON.stringify(error.body, null, 2));
    }
    if (error.code === 'object_not_found') {
      console.error('Database not found. Please check your NOTION_DATABASE_ID in .env file');
    }
    throw error;
  }
}

// Run if called directly
if (require.main === module) {
  createPageInHOMEDatabase()
    .then(() => console.log('🚀 AUTOCREATE Notion integration test completed successfully!'))
    .catch(() => process.exit(1));
}

module.exports = { createPageInHOMEDatabase };
