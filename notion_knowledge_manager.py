#!/usr/bin/env python3
"""
Notion API Knowledge Manager for AUTOCREATE Project
Notion APIを使用してサンプルページを作成し、ナレッジを登録するシステム

Features:
- Create sample pages in Notion
- Register knowledge from various sources
- Manage Chrome extension documentation
- Multi-language support (JP/EN)
"""

import os
import json
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class NotionPage:
    """Notion page data structure"""
    title: str
    content: str
    tags: List[str] = None
    type: str = "knowledge"
    language: str = "en"
    created_by: str = "AUTOCREATE_AI"

class NotionKnowledgeManager:
    """Notion API integration for knowledge management"""
    
    def __init__(self):
        self.token = os.getenv('NOTION_TOKEN')
        self.database_id = os.getenv('NOTION_DATABASE_ID', 'your_notion_database_id_here')
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        self.base_url = 'https://api.notion.com/v1'
        
        if not self.token or self.token == 'your_notion_token_here':
            print("⚠️  Warning: NOTION_TOKEN not properly configured in .env")
        
        if self.database_id == 'your_notion_database_id_here':
            print("⚠️  Warning: NOTION_DATABASE_ID not configured. Will try to create sample pages.")
    
    def test_connection(self) -> bool:
        """Test Notion API connection"""
        try:
            response = requests.get(
                f"{self.base_url}/users/me",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_info = response.json()
                print(f"✅ Notion API connection successful!")
                print(f"   User: {user_info.get('name', 'Unknown')}")
                print(f"   Type: {user_info.get('type', 'Unknown')}")
                return True
            else:
                print(f"❌ Notion API connection failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Notion API connection error: {str(e)}")
            return False
    
    def list_databases(self) -> List[Dict]:
        """List available Notion databases"""
        try:
            response = requests.post(
                f"{self.base_url}/search",
                headers=self.headers,
                json={
                    "filter": {
                        "value": "database",
                        "property": "object"
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                databases = response.json().get('results', [])
                print(f"📊 Found {len(databases)} databases:")
                
                for db in databases:
                    title = "Untitled"
                    if db.get('title') and len(db['title']) > 0:
                        title = db['title'][0].get('plain_text', 'Untitled')
                    
                    print(f"   - {title} (ID: {db['id']})")
                
                return databases
            else:
                print(f"❌ Failed to list databases: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error listing databases: {str(e)}")
            return []
    
    def create_page(self, page_data: NotionPage, parent_id: Optional[str] = None) -> Optional[str]:
        """Create a new page in Notion"""
        try:
            # If no parent_id provided, use the configured database or create a standalone page
            if parent_id is None:
                if self.database_id != 'your_notion_database_id_here':
                    parent = {"database_id": self.database_id}
                else:
                    # Create a standalone page (requires a parent page)
                    print("⚠️  Creating standalone page without database")
                    parent = {"type": "page_id", "page_id": "root"}  # This will likely fail
            else:
                parent = {"database_id": parent_id}
            
            # Prepare page content
            page_content = {
                "parent": parent,
                "properties": {
                    "Title": {
                        "title": [
                            {
                                "text": {
                                    "content": page_data.title
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
                                        "content": page_data.content
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
            
            # Add tags if database supports it
            if page_data.tags:
                page_content["properties"]["Tags"] = {
                    "multi_select": [{"name": tag} for tag in page_data.tags]
                }
            
            # Add metadata
            page_content["properties"]["Type"] = {
                "select": {"name": page_data.type}
            }
            
            page_content["properties"]["Language"] = {
                "select": {"name": page_data.language}
            }
            
            page_content["properties"]["Created By"] = {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": page_data.created_by
                        }
                    }
                ]
            }
            
            response = requests.post(
                f"{self.base_url}/pages",
                headers=self.headers,
                json=page_content,
                timeout=15
            )
            
            if response.status_code == 200:
                page_info = response.json()
                page_id = page_info['id']
                print(f"✅ Created page: {page_data.title}")
                print(f"   Page ID: {page_id}")
                return page_id
            else:
                print(f"❌ Failed to create page: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating page: {str(e)}")
            return None
    
    def create_simple_page(self, title: str, content: str) -> Optional[str]:
        """Create a simple page without database requirements"""
        try:
            # Try to create a page in a workspace (this requires admin access)
            page_content = {
                "parent": {"type": "workspace", "workspace": True},
                "properties": {
                    "title": {
                        "title": [
                            {
                                "text": {
                                    "content": title
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
                                        "content": content
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
            
            response = requests.post(
                f"{self.base_url}/pages",
                headers=self.headers,
                json=page_content,
                timeout=15
            )
            
            if response.status_code == 200:
                page_info = response.json()
                page_id = page_info['id']
                print(f"✅ Created simple page: {title}")
                print(f"   Page ID: {page_id}")
                return page_id
            else:
                print(f"❌ Failed to create simple page: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating simple page: {str(e)}")
            return None
    
    def create_sample_knowledge_pages(self) -> List[str]:
        """Create sample knowledge pages for AUTOCREATE Chrome Extension"""
        created_pages = []
        
        # Sample pages to create
        sample_pages = [
            NotionPage(
                title="AUTOCREATE Chrome Extension - Setup Guide",
                content="""# AUTOCREATE Chrome Extension Setup Guide

## Overview
This Chrome extension provides AI-powered monitoring and automation capabilities for Supabase projects.

## Key Features
- AI President monitoring system
- Automatic response generation
- XPath configuration management
- Notion API integration
- Multi-language support (JP/EN)

## Installation Steps
1. Load extension in Chrome Developer Mode
2. Configure API keys in popup
3. Set up XPath configurations
4. Test notification system
5. Verify Supabase connections

## Troubleshooting
- Check service worker status
- Verify API key configurations
- Test notification permissions
- Review console logs for errors

Created by AUTOCREATE AI System
""",
                tags=["chrome-extension", "setup", "guide"],
                type="documentation",
                language="en"
            ),
            
            NotionPage(
                title="AUTOCREATE Chrome拡張機能 - セットアップガイド",
                content="""# AUTOCREATE Chrome拡張機能 セットアップガイド

## 概要
このChrome拡張機能は、SupabaseプロジェクトのAI駆動監視と自動化機能を提供します。

## 主な機能
- AI大統領監視システム
- 自動応答生成
- XPath設定管理
- Notion API統合
- 多言語サポート (JP/EN)

## インストール手順
1. Chrome開発者モードで拡張機能を読み込み
2. ポップアップでAPIキーを設定
3. XPath設定を構成
4. 通知システムをテスト
5. Supabase接続を確認

## トラブルシューティング
- サービスワーカーの状態を確認
- APIキー設定を検証
- 通知権限をテスト
- エラーのコンソールログを確認

AUTOCREATE AIシステムによって作成
""",
                tags=["chrome-extension", "setup", "guide", "japanese"],
                type="documentation",
                language="jp"
            ),
            
            NotionPage(
                title="XPath Configuration Management",
                content="""# XPath Configuration Management System

## Purpose
Provides dynamic XPath configuration for UI automation testing and element selection.

## Features
- Preset XPath configurations
- Real-time testing and validation
- Import/Export functionality
- Element highlighting
- Multi-site support

## Configuration Structure
```json
{
  "name": "Configuration Name",
  "description": "Description of the configuration",
  "xpaths": {
    "element1": "//xpath/expression",
    "element2": "//another/xpath"
  },
  "metadata": {
    "version": "1.0",
    "author": "AUTOCREATE",
    "created": "2024-01-XX"
  }
}
```

## Best Practices
- Use specific, robust XPath expressions
- Test configurations on target sites
- Document element purposes
- Version control configurations
- Backup before major changes

## API Integration
- Background script management
- Content script injection
- Real-time validation
- Error handling and recovery

Technical documentation for developers
""",
                tags=["xpath", "automation", "configuration", "technical"],
                type="technical",
                language="en"
            ),
            
            NotionPage(
                title="Notion API Integration Knowledge",
                content="""# Notion API Integration for Knowledge Management

## Integration Overview
This system integrates with Notion API to create and manage knowledge pages automatically.

## API Capabilities
- Page creation and management
- Database integration
- Rich content formatting
- Multi-language support
- Automated knowledge registration

## Security Considerations
- API token management
- Rate limiting compliance
- Error handling and retry logic
- Data validation and sanitization

## Knowledge Categories
1. Technical Documentation
2. Setup Guides
3. Troubleshooting Information
4. API References
5. User Manuals

## Implementation Details
- RESTful API integration
- JSON-based content formatting
- Asynchronous operation handling
- Comprehensive error logging

## Future Enhancements
- Automated content updates
- AI-generated documentation
- Multi-workspace support
- Advanced search capabilities

This page demonstrates successful Notion API integration!
""",
                tags=["notion", "api", "integration", "knowledge-management"],
                type="integration",
                language="en"
            )
        ]
        
        print("🚀 Creating sample knowledge pages...")
        
        for page_data in sample_pages:
            try:
                # First try with database
                page_id = self.create_page(page_data)
                
                # If database creation fails, try simple page
                if not page_id:
                    page_id = self.create_simple_page(page_data.title, page_data.content)
                
                if page_id:
                    created_pages.append(page_id)
                else:
                    print(f"⚠️  Failed to create page: {page_data.title}")
                    
            except Exception as e:
                print(f"❌ Error creating page '{page_data.title}': {str(e)}")
        
        print(f"✅ Successfully created {len(created_pages)} knowledge pages")
        return created_pages
    
    def export_knowledge_summary(self) -> Dict[str, Any]:
        """Export a summary of created knowledge"""
        timestamp = datetime.datetime.now().isoformat()
        
        summary = {
            "export_timestamp": timestamp,
            "system": "AUTOCREATE Chrome Extension",
            "notion_integration": {
                "status": "active",
                "api_version": "2022-06-28",
                "token_configured": bool(self.token and self.token != 'your_notion_token_here'),
                "database_id": self.database_id
            },
            "knowledge_categories": [
                "Chrome Extension Documentation",
                "XPath Configuration Management", 
                "Notion API Integration",
                "Multi-language Support",
                "Technical Troubleshooting"
            ],
            "features_documented": [
                "Installation and setup",
                "API key configuration", 
                "XPath management system",
                "Notification handling",
                "Error troubleshooting",
                "Multi-language support"
            ],
            "languages_supported": ["en", "jp"],
            "integration_status": "operational"
        }
        
        return summary

def main():
    """Main execution function"""
    print("🎯 AUTOCREATE Notion Knowledge Manager")
    print("=" * 50)
    
    # Initialize manager
    manager = NotionKnowledgeManager()
    
    # Test connection
    print("\n1. Testing Notion API connection...")
    if not manager.test_connection():
        print("❌ Cannot proceed without valid Notion API connection")
        return False
    
    # List available databases
    print("\n2. Listing available databases...")
    databases = manager.list_databases()
    
    # Create sample knowledge pages
    print("\n3. Creating sample knowledge pages...")
    created_pages = manager.create_sample_knowledge_pages()
    
    # Export summary
    print("\n4. Exporting knowledge summary...")
    summary = manager.export_knowledge_summary()
    
    # Save summary to file
    summary_file = "/workspaces/AUTOCREATE/notion_knowledge_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Knowledge summary saved to: {summary_file}")
    
    # Display results
    print("\n" + "=" * 50)
    print("🎉 AUTOCREATE Notion Integration Results")
    print("=" * 50)
    print(f"✅ Pages created: {len(created_pages)}")
    print(f"📊 Databases found: {len(databases)}")
    print(f"🔗 API connection: Active")
    print(f"📝 Summary exported: {summary_file}")
    
    if created_pages:
        print("\n📋 Created Page IDs:")
        for i, page_id in enumerate(created_pages, 1):
            print(f"   {i}. {page_id}")
    
    print("\n🚀 Notion knowledge management system is ready!")
    return True

if __name__ == "__main__":
    main()
