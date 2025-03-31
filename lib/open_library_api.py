import requests
import json
from typing import List, Dict, Union

class BookSearch:
    BASE_URL = "https://openlibrary.org/search.json"
    
    def __init__(self):
        self.default_fields = ["title", "author_name", "first_publish_year", "publisher", "isbn"]
        self.default_limit = 3
    
    def _format_search_term(self, term: str) -> str:
        """Format search term for URL by replacing spaces with plus signs."""
        return term.strip().replace(" ", "+")
    
    def _build_url(self, search_term: str, search_type: str = "title", 
                 fields: List[str] = None, limit: int = None) -> str:
        """Construct the API request URL."""
        fields = fields or self.default_fields
        limit = limit or self.default_limit
        
        formatted_term = self._format_search_term(search_term)
        fields_str = ",".join(fields)
        
        return (f"{self.BASE_URL}?{search_type}={formatted_term}"
                f"&fields={fields_str}&limit={limit}")
    
    def search_books(self, search_term: str, search_type: str = "title", 
                   fields: List[str] = None, limit: int = None) -> Dict:
        """Search for books using the Open Library API."""
        url = self._build_url(search_term, search_type, fields, limit)
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises exception for 4XX/5XX errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None
    
    def format_search_results(self, api_response: Dict) -> str:
        """Format the API response into a readable string."""
        if not api_response or not api_response.get("docs"):
            return "No results found."
        
        formatted_results = []
        for book in api_response["docs"]:
            result = [
                f"Title: {book.get('title', 'Unknown')}",
                f"Author(s): {', '.join(book.get('author_name', ['Unknown']))}",
                f"First Published: {book.get('first_publish_year', 'Unknown')}",
                f"Publisher: {', '.join(book.get('publisher', ['Unknown']))}",
                f"ISBN: {', '.join(book.get('isbn', ['Unknown']))[:3]}..."  # Show first 3 ISBNs
            ]
            formatted_results.append("\n".join(result))
        
        return "\n\n".join(formatted_results)
    
    def interactive_search(self):
        """Run an interactive book search session."""
        print("Open Library Book Search")
        print("Enter 'quit' to exit\n")
        
        while True:
            search_term = input("Enter a book title or author: ").strip()
            if search_term.lower() == 'quit':
                break
            
            search_type = input("Search by [t]itle or [a]uthor? (t/a): ").strip().lower()
            search_type = "author" if search_type == 'a' else "title"
            
            limit = input("Number of results (1-10, default 3): ").strip()
            try:
                limit = min(max(1, int(limit)), 10) if limit else 3
            except ValueError:
                limit = 3
            
            response = self.search_books(search_term, search_type, limit=limit)
            formatted = self.format_search_results(response)
            
            print("\nSearch Results:")
            print(formatted)
            print("-" * 50 + "\n")


if __name__ == "__main__":
    searcher = BookSearch()
    searcher.interactive_search()