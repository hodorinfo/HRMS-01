import json

with open("/home/hodorinfo1/Downloads/HRMS_02/HRMS_01/identity_openapi.json") as f:
    spec = json.load(f)

out = """# Identity Service API Documentation

Complete API reference for Identity Service.

**Service:** Identity Service  
**Port:** 8000 (Internal) / 8001 (Mapped)  
**Base URL (Direct):** `http://localhost:8001`  
**Base URL (Gateway):** `http://192.168.1.41` (via Nginx)  
**Container:** `hrms_01-identity-service-1`

**Authentication:** JWT Bearer Token (all API endpoints except health/login)  
**Schema:** `horilla_identity` (PostgreSQL)

---

## Endpoints
"""

def resolve_ref(ref, spec):
    parts = ref.split("/")
    res = spec
    for p in parts[1:]:
        res = res[p]
    return res

def format_schema(schema, spec, depth=0):
    if "$ref" in schema:
        schema = resolve_ref(schema["$ref"], spec)
    
    if schema.get("type") == "object" and "properties" in schema:
        props = schema["properties"]
        res = "{\n"
        for k, v in props.items():
            if "$ref" in v:
                v = resolve_ref(v["$ref"], spec)
            type_str = v.get("type", "string")
            if type_str == "array":
                res += "  " * (depth + 1) + f'"{k}": [{type_str}],\n'
            else:
                res += "  " * (depth + 1) + f'"{k}": "{type_str}",\n'
        res += "  " * depth + "}"
        return res
    return "{}"

for path, methods in spec["paths"].items():
    for method, details in methods.items():
        summary = details.get('summary', path)
        description = details.get('description', 'No description provided.')
        out += f"\n### {summary}\n\n"
        out += f"**{method.upper()}** `{path}`\n\n"
        out += f"**Description:** {description}\n\n"
        
        # Parameters
        if "parameters" in details:
            out += "**Query Parameters:**\n"
            for p in details["parameters"]:
                if p["in"] == "query":
                    out += f"- `{p['name']}` ({p.get('schema', {}).get('type', 'string')})\n"
            out += "\n"
            
        # Request Body
        if "requestBody" in details:
            content = details["requestBody"].get("content", {})
            if "application/json" in content:
                schema = content["application/json"].get("schema", {})
                out += "**Request Body Example:**\n```json\n"
                out += format_schema(schema, spec)
                out += "\n```\n\n"
            elif "application/x-www-form-urlencoded" in content:
                out += "**Request Body (Form):** Required fields according to OAuth2 password flow.\n\n"
                
        out += f"**Request (Gateway):**\n"
        out += f"```bash\ncurl -X {method.upper()} http://192.168.1.41/api/v1{path.replace('/api/v1', '')} \\\n  -H \"Authorization: Bearer <token>\"\n```\n\n"
        
        # Response
        if "responses" in details:
            success_res = details["responses"].get("200") or details["responses"].get("201")
            if success_res and "content" in success_res and "application/json" in success_res["content"]:
                schema = success_res["content"]["application/json"].get("schema", {})
                out += "**Response Example (Success):**\n```json\n"
                out += format_schema(schema, spec)
                out += "\n```\n\n"
            else:
                out += "**Response:** Standard Success Response\n\n"
            
            # Error Responses
            err_codes = [c for c in details["responses"].keys() if str(c).startswith("4") or str(c).startswith("5")]
            if err_codes:
                out += "**Error Responses:**\n"
                for code in err_codes:
                    out += f"- `{code}`: {details['responses'][code].get('description', 'Error')}\n"
                out += "\n"

with open("/home/hodorinfo1/Downloads/HRMS_02/HRMS_01/identity-service/API_DOCS.md", "w") as f:
    f.write(out)

