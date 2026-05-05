import json
from api.main import app

def generate_markdown_docs():
    # 1. Pull the live OpenAPI schema directly from your FastAPI app
    schema = app.openapi()
    
    md_lines = []
    md_lines.append(f"# {schema['info']['title']} v{schema['info']['version']}")
    md_lines.append(f"*{schema['info'].get('description', 'Auto-generated API documentation')}*\n")
    md_lines.append("---\n")

    # 2. Loop through every route in your API
    for path, path_data in schema.get("paths", {}).items():
        for method, method_data in path_data.items():
            md_lines.append(f"### `{method.upper()}` {path}")
            
            summary = method_data.get('summary', '')
            if summary:
                md_lines.append(f"**Summary:** {summary}\n")

            # Extract expected form data / parameters
            request_body = method_data.get("requestBody", {})
            if request_body:
                md_lines.append("**Request Requirements:**")
                md_lines.append("- `multipart/form-data` expected.")
            
            # Extract Responses
            md_lines.append("\n**Responses:**")
            for status_code, response_data in method_data.get("responses", {}).items():
                description = response_data.get('description', 'No description')
                md_lines.append(f"- **{status_code}:** {description}")
            
            md_lines.append("\n---\n")

    # 3. Write it to a Markdown file
    with open("API_DOCS.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    print("✅ Successfully generated API_DOCS.md!")

if __name__ == "__main__":
    generate_markdown_docs()