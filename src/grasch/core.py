"""
Core Grasch session and configuration management.
"""

import os
import tempfile
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .catalog import Catalog
from .kuzu_mock import MockKuzuConnection


class LanguageLevel(Enum):
    GQL = "gql"
    LEX = "lex"


class LEXCompatibility(Enum):
    FULL = "full"
    LIMITED = "limited"
    NONE = "none"


@dataclass
class ProfileConfiguration:
    """Defines a specific GQL/LEX profile"""
    name: str
    optional_features: set[str]
    implementation_defined: Dict[str, Any]
    lex_compatibility: LEXCompatibility


@dataclass
class SessionConfiguration:
    """Session-level configuration"""
    profile: ProfileConfiguration
    language_level: LanguageLevel
    catalog_root: str = "file:."  # IRI for catalog base location
    default_catalog_path: Optional[str] = "/"  # Path relative to catalog_root
    nested_record_schema_processor_type: str = "JSON Schema"
    nested_record_schema_processor: Optional[str] = "default"


class GraschSession:
    """Main Grasch session with profile and language level configuration"""
    
    def __init__(self, config: SessionConfiguration, database_path: str):
        self.config = config
        self.database_path = database_path
        self.catalog = Catalog(database_path)
        self.kuzu_connection = MockKuzuConnection(database_path)
    
    def create_catalog_structure(self):
        """Create hierarchical catalog structure"""
        print("Creating catalog structure...")
        
        # Create directories
        self.catalog.create_directory("/production")
        self.catalog.create_directory("/production/customer_data")
        self.catalog.create_directory("/development")
        self.catalog.create_directory("/development/test_schemas")
        
        print("✓ Created catalog directories")
    
    def demonstrate_cypher_queries(self):
        """Demonstrate querying the graph using Cypher commands"""
        print("\nDemonstrating Cypher queries...")
        print("=" * 50)
        
        # Query 1: Find all persons
        print("\n1. Find all persons:")
        query1 = "MATCH (p:Person) RETURN p.name, p.age, p.email"
        results1 = self.kuzu_connection.execute(query1)
        for result in results1:
            print(f"   {result}")
        
        # Query 2: Find all companies
        print("\n2. Find all companies:")
        query2 = "MATCH (c:Company) RETURN c.name, c.industry"
        results2 = self.kuzu_connection.execute(query2)
        for result in results2:
            print(f"   {result}")
        
        # Query 3: Find employment relationships
        print("\n3. Find employment relationships:")
        query3 = "MATCH (p:Person)-[r:WORKS_FOR]->(c:Company) RETURN p.name, r.position, r.start_date, c.name"
        results3 = self.kuzu_connection.execute(query3)
        for result in results3:
            print(f"   {result}")
        
        # Query 4: Find people in technology industry
        print("\n4. Find people working in technology:")
        query4 = """
        MATCH (p:Person)-[r:WORKS_FOR]->(c:Company)
        WHERE c.industry = 'Technology'
        RETURN p.name, r.position, c.name
        """
        results4 = self.kuzu_connection.execute(query4)
        for result in results4:
            print(f"   {result}")
    
    def demonstrate_spectral_typing(self):
        """Demonstrate spectral typing and multi-conformance concepts"""
        print("\nDemonstrating spectral typing concepts...")
        print("=" * 50)
        
        print("\n1. Content Type Conformance:")
        print("   Content record: (:Person {name:'John Doe'})")
        print("   Could conform to multiple content types:")
        print("   - (:Person {name::STRING NOT NULL, age::INTEGER})")
        print("   - (:Person {name::STRING NOT NULL, age::INTEGER, email::STRING})")
        print("   - (:Person {name::STRING NOT NULL, department::STRING})")
        
        print("\n2. Key Label Disambiguation:")
        print("   With ALL ELEMENT TYPES KEYED constraint:")
        print("   - Each content type has a unique key label set")
        print("   - Eliminates multi-conformance ambiguity")
        print("   - Person type key: [Person]")
        print("   - Company type key: [Company]")
        print("   - WORKS_FOR edge type key: [WORKS_FOR]")
        
        print("\n3. Type Key Inheritance:")
        print("   Node type (Person): TK((Person)) = TK(PersonContent) = [Person]")
        print("   Edge type (WORKS_FOR): TK((Person)-[WORKS_FOR]->(Company)) = TK(EmploymentContent) = [WORKS_FOR]")