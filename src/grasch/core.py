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


class LanguageTypes(Enum):
    """
    Value type system enumeration - orthogonal to LanguageLevel.
    
    Controls which type system is used for value validation and inference.
    Can be mixed with any LanguageLevel (e.g., GQL with Cypher types).
    """
    GQL = "gql"           # GQL property value types (full precision)
    SQL = "sql"           # SQL Foundation data types  
    JSON = "json"         # Basic JSON Schema types (number, string, boolean, object, array, null)
    DATABASE_JSON = "database_json"  # Extended database JSON types (1-to-1 with GQL)
    CYPHER = "cypher"     # Cypher data types (limited precision)


class LEXCompatibility(Enum):
    FULL = "full"
    LIMITED = "limited"
    NONE = "none"


@dataclass
class CatalogRootConfiguration:
    """Configuration for catalog root IRI and path resolution"""
    catalogRoot: str = "file:."
    supportedSchemes: set[str] = None
    
    def __post_init__(self):
        if self.supportedSchemes is None:
            self.supportedSchemes = {"file"}
    
    def resolvePath(self, relativePath: str) -> str:
        """Combine catalogRoot IRI with relative path"""
        if self.catalogRoot.startswith("file:"):
            # Handle file: scheme resolution
            basePath = self.catalogRoot[5:]  # Remove "file:" prefix
            if basePath == ".":
                return relativePath
            return f"{basePath}/{relativePath.lstrip('/')}"
        else:
            # Handle other IRI schemes
            return f"{self.catalogRoot.rstrip('/')}/{relativePath.lstrip('/')}"
    
    def validateIri(self, iri: str) -> bool:
        """Validate that IRI uses supported scheme"""
        scheme = iri.split(":", 1)[0] if ":" in iri else ""
        return scheme in self.supportedSchemes


@dataclass
class ProfileConfiguration:
    """Defines a specific GQL/LEX profile"""
    name: str
    optionalFeatures: set[str]
    implementationDefined: Dict[str, Any]
    lexCompatibility: LEXCompatibility


@dataclass
class SessionConfiguration:
    """Session-level configuration"""
    profile: ProfileConfiguration
    languageLevel: LanguageLevel
    catalogRoot: str = "file:."  # IRI for catalog base location
    defaultCatalogPath: Optional[str] = "/"  # Path relative to catalogRoot
    nestedRecordSchemaProcessorType: str = "JSON Schema"
    nestedRecordSchemaProcessor: Optional[str] = "default"


class GraschSession:
    """Main Grasch session with profile and language level configuration"""
    
    def __init__(self, config: SessionConfiguration, databasePath: str):
        self.config = config
        self.databasePath = databasePath
        
        # Initialize catalog root configuration
        self.catalogRootConfig = CatalogRootConfiguration(
            catalogRoot=config.catalogRoot
        )
        
        # Validate catalog root IRI
        if not self.catalogRootConfig.validateIri(config.catalogRoot):
            raise ValueError(f"Unsupported IRI scheme in catalogRoot: {config.catalogRoot}")
        
        self.catalog = Catalog(databasePath, self.catalogRootConfig)
        self.kuzuConnection = MockKuzuConnection(databasePath)
    
    def createCatalogStructure(self):
        """Create hierarchical catalog structure"""
        print("Creating catalog structure...")
        
        # Create directories
        self.catalog.createDirectory("/production")
        self.catalog.createDirectory("/production/customer_data")
        self.catalog.createDirectory("/development")
        self.catalog.createDirectory("/development/test_schemas")
        
        print("✓ Created catalog directories")
    
    def demonstrateCypherQueries(self):
        """Demonstrate querying the graph using Cypher commands"""
        print("\nDemonstrating Cypher queries...")
        print("=" * 50)
        
        # Query 1: Find all persons
        print("\n1. Find all persons:")
        query1 = "MATCH (p:Person) RETURN p.name, p.age, p.email"
        results1 = self.kuzuConnection.execute(query1)
        for result in results1:
            print(f"   {result}")
        
        # Query 2: Find all companies
        print("\n2. Find all companies:")
        query2 = "MATCH (c:Company) RETURN c.name, c.industry"
        results2 = self.kuzuConnection.execute(query2)
        for result in results2:
            print(f"   {result}")
        
        # Query 3: Find employment relationships
        print("\n3. Find employment relationships:")
        query3 = "MATCH (p:Person)-[r:WORKS_FOR]->(c:Company) RETURN p.name, r.position, r.start_date, c.name"
        results3 = self.kuzuConnection.execute(query3)
        for result in results3:
            print(f"   {result}")
        
        # Query 4: Find people in technology industry
        print("\n4. Find people working in technology:")
        query4 = """
        MATCH (p:Person)-[r:WORKS_FOR]->(c:Company)
        WHERE c.industry = 'Technology'
        RETURN p.name, r.position, c.name
        """
        results4 = self.kuzuConnection.execute(query4)
        for result in results4:
            print(f"   {result}")
    
    def demonstrateSpectralTyping(self):
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