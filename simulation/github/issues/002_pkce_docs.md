# Issue #208 — PKCE is missing from OAuth documentation

**Status:** open  
**Author:** @dev-jordan  
**Labels:** documentation, oauth, security

## Description

Authly `0.3.0` requires PKCE for public clients.

The current OAuth documentation does not explain:

- code verifier
- code challenge
- S256
- when PKCE is required
- how the Python SDK generates the challenge

## Expected

Add a complete PKCE example.

## Environment

Authly `0.3.0`
