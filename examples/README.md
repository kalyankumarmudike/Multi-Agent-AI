# Examples

Sample code demonstrating how to use the Multi-Agent Document Intelligence System.

## Sample Client (`sample_client.py`)

A Python client that demonstrates:
- Health check
- Document analysis
- Result parsing and display
- Error handling

### Usage

1. Make sure the API server is running:
```bash
cd backend
uvicorn app.main:app --reload
```

2. Run the sample client:
```bash
python examples/sample_client.py
```

### Output

The client will:
- Check API health
- Analyze a sample document
- Display formatted results
- Save results to `analysis_results.json`

## Customization

Modify `sample_document` in `sample_client.py` to analyze your own documents.

## Integration Examples

### Python with Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/analyze-document",
    json={"document_text": "Your document here..."}
)
result = response.json()
```

### Python with httpx (async)

```python
import httpx
import asyncio

async def analyze():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/analyze-document",
            json={"document_text": "Your document here..."}
        )
        return response.json()

result = asyncio.run(analyze())
```

### JavaScript/TypeScript

```typescript
const response = await fetch('http://localhost:8000/analyze-document', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    document_text: "Your document here..."
  })
});

const result = await response.json();
```

### cURL

```bash
curl -X POST "http://localhost:8000/analyze-document" \
  -H "Content-Type: application/json" \
  -d '{"document_text": "Your document here..."}'
```

## Response Format

```json
{
  "summary": "Comprehensive summary...",
  "action_items": [
    {
      "task": "Complete dashboard redesign",
      "owner": "Sarah",
      "deadline": "February 15th",
      "dependencies": []
    }
  ],
  "risks_and_open_issues": [
    {
      "issue": "Infrastructure capacity at 80%",
      "type": "risk",
      "impact": "high"
    }
  ]
}
```
