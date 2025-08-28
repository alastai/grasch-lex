"""
Mock Kuzu database connection for demonstration purposes.
"""

from typing import List, Dict, Any


class MockKuzuConnection:
    """Mock Kuzu database connection for demonstration"""
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.nodes = []
        self.edges = []
    
    def execute(self, query: str) -> List[Dict[str, Any]]:
        """Execute a Cypher query (simplified mock implementation)"""
        print(f"Executing Cypher query: {query}")
        
        # Mock query results for demonstration
        if "MATCH (p:Person)" in query:
            return [
                {"p.name": "Alice Johnson", "p.age": 30, "p.email": "alice@example.com"},
                {"p.name": "Bob Smith", "p.age": 25, "p.email": "bob@example.com"}
            ]
        elif "MATCH (c:Company)" in query:
            return [
                {"c.name": "TechCorp", "c.industry": "Technology"},
                {"c.name": "DataSystems", "c.industry": "Software"}
            ]
        elif "MATCH (p:Person)-[r:WORKS_FOR]->(c:Company)" in query:
            return [
                {"p.name": "Alice Johnson", "r.position": "Engineer", "r.start_date": "2020-01-15", "c.name": "TechCorp"},
                {"p.name": "Bob Smith", "r.position": "Analyst", "r.start_date": "2021-03-01", "c.name": "DataSystems"}
            ]
        else:
            return []