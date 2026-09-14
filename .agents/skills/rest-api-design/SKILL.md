---
name: rest-api-design
description: >
  Design RESTful APIs following best practices for resource modeling, HTTP
  methods, status codes, versioning, and documentation. Use when creating new
  APIs, designing endpoints, or improving existing API architecture.
---

# REST API Design

## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Reference Guides](#reference-guides)
- [Best Practices](#best-practices)

## Overview

Design REST APIs that are intuitive, consistent, and follow industry best practices for resource-oriented architecture.

## When to Use

- Designing new RESTful APIs
- Creating endpoint structures
- Defining request/response formats
- Implementing API versioning
- Documenting API specifications
- Refactoring existing APIs

## Quick Start

Minimal working example:

```
✅ Good Resource Names (Nouns, Plural)
GET    /api/users
GET    /api/users/123
GET    /api/users/123/orders
POST   /api/products
DELETE /api/products/456

❌ Bad Resource Names (Verbs, Inconsistent)
GET    /api/getUsers
POST   /api/createProduct
GET    /api/user/123  (inconsistent singular/plural)
```

## Reference Guides

Detailed implementations in the `references/` directory:

| Guide | Contents |
|---|---|---|
| [Resource Naming](references/resource-naming.md) | Resource Naming, HTTP Methods & Operations |
| [Request Examples](references/request-examples.md) | Request Examples |
| [Query Parameters](references/query-parameters.md) | Query Parameters |
| [Response Formats](references/response-formats.md) | Response Formats |
| [HTTP Status Codes](references/http-status-codes.md) | HTTP Status Codes, API Versioning, Authentication & Security, Rate Limiting Headers |
| [OpenAPI Documentation](references/openapi-documentation.md) | OpenAPI Documentation |
| [Complete Example: Express.js](references/complete-example-expressjs.md) | const express = require("express"); |
| [FastAPI Conventions (this project)](references/fastapi-conventions.md) | Convenciones y status codes aplicados a este repo (FastAPI + Clean Architecture); template en `templates/endpoint_fastapi.py` |

## Applying to FastAPI (this project)

Este repositorio (`api_normalizacion_afiliados`) es una API REST FastAPI con Clean Architecture + Hexagonal. Antes de diseñar endpoints nuevos, leer `references/fastapi-conventions.md`: ahí está el mapeo excepción de dominio → HTTP del `handlers.py` real, el naming vigente (`/afiliados`, `/sync/sheets/import`) y las inconsistencias detectadas. Usar `templates/endpoint_fastapi.py` como scaffold de endpoint y seguir `.agents/rules/reglas-solid.md` (SRP, ports, DI).

## Best Practices

### ✅ DO

- Use nouns for resources, not verbs
- Use plural names for collections
- Be consistent with naming conventions
- Return appropriate HTTP status codes
- Include pagination for collections
- Provide filtering and sorting options
- Version your API
- Document thoroughly with OpenAPI
- Use HTTPS
- Implement rate limiting
- Provide clear error messages
- Use ISO 8601 for dates

### ❌ DON'T

- Use verbs in endpoint names
- Return 200 for errors
- Expose internal IDs unnecessarily
- Over-nest resources (max 2 levels)
- Use inconsistent naming
- Forget authentication
- Return sensitive data
- Break backward compatibility without versioning
