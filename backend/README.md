# Inventory Management & Procurement System (POC-07)

## Associate Details

- Name: Panuganti Madhusudan
- POC ID: POC-07
- Phase: Phase 1 – Core Inventory Management System

---

## Project Overview

The Inventory Management & Procurement System is a FastAPI-based backend application designed to manage products, suppliers, inventory stock levels, and purchase orders.

The application provides secure authentication, inventory tracking, procurement workflows, observability logging, and dashboard reporting.

---

## Technology Stack

### Backend

- FastAPI
- SQLAlchemy
- SQLite

### Authentication

- JWT Authentication
- Passlib (bcrypt)

### Observability

- Structlog
- OpenTelemetry
- Request Logging Middleware
- Distributed Tracing

### Testing

- Pytest

---

## Key Features

### Authentication

- User Registration
- User Login
- JWT Token Validation

### Supplier Management

- Create Supplier
- View Supplier Details
- Supplier Catalog

### Product Management

- Create Product
- Get Products
- Get Product Details
- Update Stock Levels

### Purchase Orders

- Create Purchase Order
- Receive Purchase Order
- Order Tracking

### Dashboard

- Inventory Dashboard
- Low Stock Alerts
- Inventory Analytics

---

## Observability Features

- Structured JSON Logging
- Request ID Tracking
- API Entry Logging
- API Exit Logging
- Login Success Logging
- Login Failure Logging
- Token Validation Logging
- Database Operation Logging
- Global Exception Logging
- OpenTelemetry FastAPI Instrumentation
- Tracing Spans:
  - http.request
  - db.query
  - auth.validate

---

## Installation

```bash
pip install -r requirements.txt