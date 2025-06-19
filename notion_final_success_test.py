import os
import requests
import json
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def create_final_notion_page():
    """Create a simple page that will definitely work with HOME database properties"""
    
    token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID', '215fd0b5-bf7d-8069-99f3-dc4db1937b76')
    
    if not token:
        print("❌ NOTION_TOKEN not found")
        return
    
    print("🎯 AUTOCREATE Final Notion Test")
    print("=" * 40)
    print(f"Database ID: {database_id}")
    
    # Create page with exact properties that exist in HOME database
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Simple page data matching HOME database schema
    page_data = {
        "parent": {
            "type": "database_id",
            "database_id": database_id
        },
        "properties": {
            "Question 1": {
                "title": [
                    {
                        "text": {
                            "content": "🎯 AUTOCREATE Notion Integration Success!"
                        }
                    }
                ]
            },
            "Question 2": {
                "multi_select": [
                    {"name": "Automation"},
                    {"name": "Knowledge Management"},
                    {"name": "Success"}
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
            }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "🎉 AUTOCREATE Notion Integration Complete!"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "This page was automatically created by the AUTOCREATE system as a demonstration of successful Notion API integration."
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "✅ Completed Features"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Chrome Extension Integration"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "XPath Configuration Management"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Notion API Rich Content Creation"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Comprehensive Error Handling"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "🚀 System Information"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"Created: {datetime.now().isoformat()}\nProject: AUTOCREATE\nStatus: Production Ready\nIntegration: n8n → Notion API"
                            }
                        }
                    ]
                }
            }
        ]
    }
    
    try:
        print("🚀 Creating final success page...")
        response = requests.post(url, headers=headers, json=page_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Page created successfully!")
            print(f"📄 Page ID: {result.get('id')}")
            print(f"🔗 Page URL: {result.get('url')}")
            print(f"📅 Created: {result.get('created_time')}")
            
            return result
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    create_final_notion_page()
