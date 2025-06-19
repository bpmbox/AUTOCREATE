#!/usr/bin/env python3
"""
Notion Workspace Explorer and Database Creator
Notionワークスペースを探索し、必要に応じてデータベースを作成するツール
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

class NotionWorkspaceExplorer:
    def __init__(self):
        self.token = os.getenv('NOTION_TOKEN')
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        self.base_url = 'https://api.notion.com/v1'
    
    def search_all_content(self):
        """Search for all accessible pages and databases"""
        print("🔍 Searching all accessible Notion content...")
        
        try:
            response = requests.post(
                f"{self.base_url}/search",
                headers=self.headers,
                json={"page_size": 100},
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json().get('results', [])
                print(f"📊 Found {len(results)} items total")
                
                pages = [r for r in results if r.get('object') == 'page']
                databases = [r for r in results if r.get('object') == 'database']
                
                print(f"📄 Pages: {len(pages)}")
                print(f"🗃️  Databases: {len(databases)}")
                
                return pages, databases
            else:
                print(f"❌ Search failed: {response.status_code}")
                print(f"Response: {response.text}")
                return [], []
                
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            return [], []
    
    def display_pages(self, pages):
        """Display found pages with details"""
        if not pages:
            print("📄 No pages found")
            return
        
        print(f"\n📄 Found {len(pages)} pages:")
        print("-" * 80)
        
        for i, page in enumerate(pages, 1):
            title = "Untitled"
            if page.get('properties'):
                # Try different title property names
                for prop_name in ['title', 'Title', 'Name', 'name']:
                    if prop_name in page['properties']:
                        prop = page['properties'][prop_name]
                        if prop.get('title') and len(prop['title']) > 0:
                            title = prop['title'][0].get('plain_text', 'Untitled')
                            break
            
            created_time = page.get('created_time', 'Unknown')
            last_edited = page.get('last_edited_time', 'Unknown')
            
            print(f"{i:2d}. {title}")
            print(f"    ID: {page['id']}")
            print(f"    Created: {created_time[:10] if created_time != 'Unknown' else 'Unknown'}")
            print(f"    Edited: {last_edited[:10] if last_edited != 'Unknown' else 'Unknown'}")
            print()
    
    def display_databases(self, databases):
        """Display found databases with details"""
        if not databases:
            print("🗃️  No databases found")
            return
        
        print(f"\n🗃️  Found {len(databases)} databases:")
        print("-" * 80)
        
        for i, db in enumerate(databases, 1):
            title = "Untitled Database"
            if db.get('title') and len(db['title']) > 0:
                title = db['title'][0].get('plain_text', 'Untitled Database')
            
            created_time = db.get('created_time', 'Unknown')
            
            print(f"{i:2d}. {title}")
            print(f"    ID: {db['id']}")
            print(f"    Created: {created_time[:10] if created_time != 'Unknown' else 'Unknown'}")
            
            # Show properties
            properties = db.get('properties', {})
            if properties:
                print(f"    Properties: {list(properties.keys())}")
            print()
    
    def create_knowledge_database(self, parent_page_id=None):
        """Create a new database for knowledge management"""
        print("🏗️  Creating AUTOCREATE Knowledge Database...")
        
        # Database schema
        database_schema = {
            "parent": {
                "type": "workspace",
                "workspace": True
            } if parent_page_id is None else {
                "type": "page_id",
                "page_id": parent_page_id
            },
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": "AUTOCREATE Knowledge Base"
                    }
                }
            ],
            "properties": {
                "Title": {
                    "title": {}
                },
                "Type": {
                    "select": {
                        "options": [
                            {"name": "Documentation", "color": "blue"},
                            {"name": "Technical", "color": "green"},
                            {"name": "Guide", "color": "yellow"},
                            {"name": "Integration", "color": "purple"},
                            {"name": "Knowledge", "color": "gray"}
                        ]
                    }
                },
                "Language": {
                    "select": {
                        "options": [
                            {"name": "en", "color": "default"},
                            {"name": "jp", "color": "red"}
                        ]
                    }
                },
                "Tags": {
                    "multi_select": {
                        "options": [
                            {"name": "chrome-extension", "color": "blue"},
                            {"name": "xpath", "color": "green"},
                            {"name": "notion", "color": "purple"},
                            {"name": "supabase", "color": "orange"},
                            {"name": "ai", "color": "red"},
                            {"name": "automation", "color": "yellow"}
                        ]
                    }
                },
                "Status": {
                    "select": {
                        "options": [
                            {"name": "Draft", "color": "gray"},
                            {"name": "In Progress", "color": "yellow"},
                            {"name": "Complete", "color": "green"},
                            {"name": "Archived", "color": "red"}
                        ]
                    }
                },
                "Created By": {
                    "rich_text": {}
                },
                "Created Date": {
                    "created_time": {}
                },
                "Last Updated": {
                    "last_edited_time": {}
                }
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/databases",
                headers=self.headers,
                json=database_schema,
                timeout=15
            )
            
            if response.status_code == 200:
                database = response.json()
                database_id = database['id']
                print(f"✅ Database created successfully!")
                print(f"   Database ID: {database_id}")
                print(f"   URL: https://notion.so/{database_id.replace('-', '')}")
                
                # Update .env file with the new database ID
                self.update_env_database_id(database_id)
                
                return database_id
            else:
                print(f"❌ Database creation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Database creation error: {str(e)}")
            return None
    
    def update_env_database_id(self, database_id):
        """Update .env file with the new database ID"""
        env_file = "/workspaces/AUTOCREATE/.env"
        
        try:
            # Read current .env file
            with open(env_file, 'r') as f:
                lines = f.readlines()
            
            # Update or add NOTION_DATABASE_ID
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('NOTION_DATABASE_ID='):
                    lines[i] = f'NOTION_DATABASE_ID={database_id}\n'
                    updated = True
                    break
            
            # If not found, add it
            if not updated:
                lines.append(f'\nNOTION_DATABASE_ID={database_id}\n')
            
            # Write back to file
            with open(env_file, 'w') as f:
                f.writelines(lines)
            
            print(f"✅ Updated .env file with database ID: {database_id}")
            
        except Exception as e:
            print(f"⚠️  Could not update .env file: {str(e)}")
    
    def create_sample_page_in_workspace(self):
        """Try to create a simple page in workspace root"""
        print("📝 Attempting to create a test page...")
        
        page_content = {
            "parent": {
                "type": "workspace",
                "workspace": True
            },
            "properties": {
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": "AUTOCREATE Test Page"
                            }
                        }
                    ]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "This is a test page created by AUTOCREATE system to verify Notion API integration."
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/pages",
                headers=self.headers,
                json=page_content,
                timeout=15
            )
            
            if response.status_code == 200:
                page = response.json()
                page_id = page['id']
                print(f"✅ Test page created!")
                print(f"   Page ID: {page_id}")
                return page_id
            else:
                print(f"❌ Test page creation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Test page creation error: {str(e)}")
            return None

def main():
    print("🚀 AUTOCREATE Notion Workspace Explorer")
    print("=" * 60)
    
    explorer = NotionWorkspaceExplorer()
    
    # Search all content
    pages, databases = explorer.search_all_content()
    
    # Display results
    explorer.display_pages(pages)
    explorer.display_databases(databases)
    
    # Try to create a database
    print("\n" + "=" * 60)
    print("🏗️  Attempting to create knowledge database...")
    
    # First try with workspace
    database_id = explorer.create_knowledge_database()
    
    # If database creation fails, try to create a test page first
    if not database_id and len(pages) == 0:
        print("\n📝 No existing pages found. Trying to create a test page...")
        test_page_id = explorer.create_sample_page_in_workspace()
        
        if test_page_id:
            print(f"✅ Test page created: {test_page_id}")
            print("   You can now use this page as a parent for creating databases")
            
            # Try to create database with the test page as parent
            database_id = explorer.create_knowledge_database(test_page_id)
    
    # If we have existing pages, suggest using one as parent
    elif not database_id and len(pages) > 0:
        print("\n💡 Suggestion: Use an existing page as parent for the database")
        print("   Available pages:")
        for i, page in enumerate(pages[:3], 1):
            title = "Untitled"
            if page.get('properties'):
                for prop_name in ['title', 'Title', 'Name', 'name']:
                    if prop_name in page['properties']:
                        prop = page['properties'][prop_name]
                        if prop.get('title') and len(prop['title']) > 0:
                            title = prop['title'][0].get('plain_text', 'Untitled')
                            break
            print(f"   {i}. {title} (ID: {page['id']})")
        
        if pages:
            print(f"\n   To create database under first page, run:")
            print(f"   python3 -c \"from notion_workspace_explorer import NotionWorkspaceExplorer; NotionWorkspaceExplorer().create_knowledge_database('{pages[0]['id']}')\"")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"📄 Pages found: {len(pages)}")
    print(f"🗃️  Databases found: {len(databases)}")
    print(f"🏗️  Database created: {'Yes' if database_id else 'No'}")
    
    if database_id:
        print(f"✅ Knowledge database ready: {database_id}")
        print("   You can now run notion_knowledge_manager.py to create sample pages")
    else:
        print("⚠️  No database created. Manual setup may be required.")
    
    print("\n🎯 Next steps:")
    if database_id:
        print("   1. Run: python3 notion_knowledge_manager.py")
        print("   2. Verify pages created in Notion")
    else:
        print("   1. Create a page manually in Notion")
        print("   2. Use page ID to create database")
        print("   3. Update NOTION_DATABASE_ID in .env")

if __name__ == "__main__":
    main()
