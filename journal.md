# Enterprise AI Knowledge Platform

## Engineering Journal

**Author:** Suel Ahmed
**Objective:** Build an enterprise-grade AI Knowledge Platform demonstrating production-ready backend engineering, AI engineering, MLOps, and system design suitable for Senior/Staff AI Engineer roles.

---

# Project Vision

The objective is **not** to build another RAG demo.

The objective is to build an enterprise AI platform that resembles what would exist inside a large organization.

By the end of the project the platform should demonstrate:

* Production backend engineering
* AI engineering
* Agentic AI
* RAG
* Enterprise architecture
* MLOps
* AI observability
* Cloud deployment
* Testing
* Scalability

Ultimately the system should support:

```
User

↓

Authentication

↓

Upload Documents

↓

Storage

↓

Text Extraction

↓

Chunking

↓

Embeddings

↓

Vector Search

↓

Hybrid Retrieval

↓

LLM

↓

Evaluation

↓

Observability

↓

Feedback

↓

Monitoring
```

---

# Guiding Engineering Principles

Throughout the project we follow several engineering principles.

## 1. Separation of Responsibilities

Every class should have one responsibility.

Examples:

* API handles HTTP.
* Service handles business logic.
* Repository handles database access.
* Storage handles files.
* Processor extracts text.

---

## 2. Build for Production

Avoid shortcuts that only work for demos.

Instead build:

* scalable architecture
* modular services
* replaceable components
* clean interfaces

---

## 3. Build Infrastructure Before AI

Most AI demos immediately call GPT.

Enterprise systems first build:

* persistence
* storage
* logging
* testing
* deployment

Only then AI.

---

## 4. Think Like an Architect

Every design decision should answer:

* Why?
* Why not another approach?
* How will this scale?

---

# Day 1 — Foundation

## Goal

Build a production-ready backend foundation.

Without this, every future feature becomes difficult.

---

## What Was Built

* FastAPI application
* Project structure
* Configuration management
* Environment variables
* Logging
* Trace ID middleware
* Docker
* PostgreSQL container
* Redis container
* Health endpoint
* Version endpoint
* Basic testing setup

---

## Problem We Were Solving

An enterprise AI system cannot rely on a single Python file.

It needs:

* repeatable setup
* consistent configuration
* observability
* infrastructure

---

## Architecture

```
Client

↓

FastAPI

↓

Middleware

↓

Routes

↓

Response
```

---

## Key Concepts Learned

### FastAPI

Responsible for HTTP.

Receives requests.

Returns responses.

Nothing else.

---

### Docker

Provides reproducible environments.

Everyone runs the same infrastructure.

Instead of installing PostgreSQL manually:

```
docker compose up
```

creates identical environments.

---

### Environment Variables

Never hardcode:

* passwords
* URLs
* API keys

Everything comes from:

```
.env
```

---

### Logging

Every production system requires logs.

Logs answer:

* What happened?
* When?
* Why?

---

### Trace ID

Every request gets a unique ID.

Useful for debugging distributed systems.

---

## Design Decisions

### Why Docker?

Instead of requiring everyone to install PostgreSQL locally.

---

### Why Redis?

Future support for:

* caching
* queues
* background jobs
* sessions

---

## Interview Explanation

> I first built the infrastructure layer because every production AI application requires reproducible environments, logging, configuration management, and observability before implementing business features.

---

## Milestone Achieved

A production-ready backend foundation.

---

# Day 2 — Persistence Layer

## Goal

Persist document metadata.

---

## Problem

After uploading a document, the application forgets it after restarting.

Need permanent storage.

---

## Solution

PostgreSQL.

---

## Architecture

```
Client

↓

API

↓

Pydantic

↓

Service

↓

Repository

↓

Session

↓

Engine

↓

PostgreSQL
```

---

## Components Built

* SQLAlchemy
* Async Engine
* Session
* Declarative Base
* Document Model
* Repository
* Service
* Alembic
* Migration
* CRUD endpoint

---

## Core Concepts

### Engine

Responsible for connecting to PostgreSQL.

Think:

> Database Connection Manager

---

### Session

Represents one conversation with the database.

Example:

```
Open

↓

Insert

↓

Update

↓

Commit

↓

Close
```

---

### Model

Python representation of a database table.

```
Document

↓

documents table
```

---

### Repository

Responsible only for:

* INSERT
* UPDATE
* DELETE
* SELECT

No business logic.

---

### Service

Responsible for orchestration.

Future examples:

* duplicate detection
* virus scan
* upload to cloud
* notifications

---

### Alembic

Database version control.

Equivalent to Git for schema changes.

---

### Migration

A migration safely changes the database.

Example:

```
Add Column

↓

Generate Migration

↓

Review

↓

Execute
```

---

## Why PostgreSQL?

Chosen because:

* production ready
* excellent SQLAlchemy support
* JSON support
* AI ecosystem standard
* future pgvector compatibility
* common in US startups

---

## Design Decisions

### Why Repository Pattern?

Avoid SQL inside API routes.

---

### Why Service Layer?

Business logic changes frequently.

Database logic should remain isolated.

---

### Why SQLAlchemy?

Provides ORM while remaining database agnostic.

---

## Interview Explanation

> We separated HTTP, business logic, and persistence into API, Service, and Repository layers. This makes the application easier to maintain and allows database changes without affecting business logic.

---

## Milestone Achieved

Application can permanently store document metadata.

---

# Day 3 — File Storage Layer

## Goal

Store actual uploaded files.

---

## Problem

Day 2 only stored metadata.

Actual PDF did not exist anywhere.

---

## Solution

Separate:

* file storage
* metadata storage

---

## Architecture

```
Upload

↓

DocumentService

├── StorageService

└── DocumentRepository

↓

uploads/

↓

PostgreSQL
```

---

## Components Built

* StorageService
* LocalStorageService
* Upload endpoint
* Upload folder
* File validation
* Metadata persistence

---

## Concepts Learned

### Metadata

Information about the document.

Examples:

* filename
* file size
* mime type
* processing status

---

### Physical File

Actual bytes.

Stored separately.

---

### StorageService

Responsible only for:

* save
* delete
* exists

No database logic.

---

## Why Separate Storage?

Future migration becomes easy.

Today:

```
Local Disk
```

Tomorrow:

```
AWS S3

Azure Blob

Google Cloud Storage
```

Only StorageService changes.

---

## Design Pattern

Dependency Inversion.

Business logic depends on an abstraction rather than local storage.

---

## Interview Explanation

> We intentionally separated physical file storage from metadata storage. This allows replacing local storage with cloud object storage without changing business logic.

---

## Milestone Achieved

Application stores both:

* file
* metadata

---

# Day 4 — Document Processing (Architecture Complete)

## Goal

Convert uploaded documents into machine-readable text.

---

## Problem

AI cannot understand PDFs.

Need extracted text.

---

## Architecture

```
Upload

↓

Storage

↓

Processor

↓

Extract Text

↓

Content Storage
```

---

## Components Designed

* Processor Interface
* PDF Processor
* DOCX Processor
* TXT Processor
* Processor Factory
* document_contents table

---

## Why Separate document_contents?

documents stores metadata.

document_contents stores large extracted text.

Advantages:

* faster metadata queries
* scalable design
* prepares for chunking

---

## Strategy Pattern

Every processor implements:

```
extract_text()
```

Supported processors:

* PDF
* DOCX
* TXT

Future:

* PPTX
* HTML
* Markdown
* Audio
* Video

---

## Factory Pattern

Instead of:

```
if pdf

elif docx

elif txt
```

Use:

```
ProcessorFactory
```

Benefits:

* cleaner code
* easier extension
* follows Open/Closed Principle

---

## Design Decisions

### Why Processor Interface?

Allows adding new formats without changing service logic.

---

### Why Factory?

Centralizes processor selection.

---

### Why Separate Content Table?

Metadata and large text have different access patterns.

---

## Interview Explanation

> The extraction layer follows the Strategy pattern where each document type implements a common extraction interface. A Factory selects the correct implementation, allowing new document formats to be added without modifying the orchestration logic.

---

## Current Overall Architecture

```
                        FastAPI

                           │

                           ▼

                   DocumentService

               ┌───────────┴────────────┐

               ▼                        ▼

        StorageService          DocumentRepository

               │                        │

               ▼                        ▼

        uploads/ folder            PostgreSQL

                           │

                           ▼

                   Extraction Layer

                           │

                    Processor Factory

         ┌────────────┬────────────┬────────────┐

         ▼            ▼            ▼

    PDF Processor  DOCX Processor  TXT Processor
```

---

# Overall Progress

| Day   | Status                                                      |
| ----- | ----------------------------------------------------------- |
| Day 1 | ✅ Complete                                                  |
| Day 2 | ✅ Complete                                                  |
| Day 3 | ✅ Complete                                                  |
| Day 4 | 🟡 Architecture complete, implementation partially complete |

---

# Tomorrow's Milestone (Finish Day 4)

## Objective

Complete the document extraction pipeline.

### Tasks

1. Implement `ExtractionService`.
2. Create `DocumentContentRepository`.
3. Create `DocumentContentService`.
4. Wire extraction into `DocumentService`.
5. Upload a PDF.
6. Extract text automatically.
7. Store extracted text in `document_contents`.
8. Update `processing_status`.
9. Add integration tests.

---

# What Day 4 Unlocks

Once Day 4 is complete:

```
Upload

↓

Extract Text

↓

Store Raw Text
```

This enables Day 5.

---

# Day 5 Preview

Document Chunking.

Pipeline becomes:

```
Raw Text

↓

Cleaning

↓

Chunking

↓

Chunk Metadata

↓

Chunk Table
```

This is the foundation for embeddings and retrieval.

---

# Day 5 — Document Chunking

## Goal

Split extracted text into manageable chunks for embeddings and LLM processing.

---

## Problem

Raw extracted text is too large.

Examples:

* 100-page document = 50,000+ tokens
* LLM context windows are limited (4k-128k tokens)
* Embeddings work best on ~512 token chunks
* Need strategy for maintaining context between chunks

---

## Solution

Implement chunking layer with:

* multiple chunking strategies (extensible)
* configurable chunk size
* overlap (context preservation)
* token estimation
* chunk metadata

---

## Architecture

```
Raw Text (document_contents)

         ↓

Chunking Service

         ↓

Chunking Strategy

├── Fixed Size Chunker

├── Sentence Chunker (future)

└── Semantic Chunker (future)

         ↓

Chunk Metadata Extraction

         ↓

DocumentChunk Model

         ↓

PostgreSQL (document_chunks table)
```

---

## Components Built

* `ChunkingStrategy` (base class)
* `FixedSizeChunker` (implementation)
* `TextChunk` (data structure)
* `DocumentChunk` (SQLAlchemy model)
* `DocumentChunkRepository` (CRUD)
* `ChunkingService` (orchestration)
* `/chunk` endpoint
* `DocumentChunkResponse` (Pydantic schema)

---

## Core Concepts

### Chunk

A segment of text with metadata:

```
{
  chunk_index: 0,
  text: "The quick brown fox...",
  start_char: 0,
  end_char: 150,
  char_count: 150,
  token_estimate: 25
}
```

---

### ChunkingStrategy

Pattern for different chunking approaches.

Current implementation:

* Fixed Size (512 chars)
* Configurable overlap (50 chars)

Future strategies:

* Sentence-based
* Paragraph-based
* Semantic (using embeddings)
* Format-aware (table rows, code blocks)

---

### Token Estimation

Estimate token count without external API.

Formula:

```
tokens ≈ char_count / 4
```

Enables:

* pre-filtering before LLM calls
* cost estimation
* context window validation

---

### Overlap

Chunks share context.

Example:

```
Chunk 0: [0-512]

Chunk 1: [462-974]   (50 char overlap)

Chunk 2: [924-1436]  (50 char overlap)
```

Benefits:

* better retrieval accuracy
* preserves context boundaries
* prevents idea fragmentation

---

## Why Separate Chunking?

Extraction creates raw content.

Chunking is independent concern.

Separation enables:

* different chunking strategies
* reprocessing with new strategy
* testing without extraction
* future async processing

---

## Design Decisions

### Why Strategy Pattern?

Chunking approaches vary:

* Fixed size (simple, reliable)
* Sentence-based (structure aware)
* Semantic (uses embeddings)
* Language-specific (CJK vs Latin)

Strategy pattern allows all approaches without if/else sprawl.

---

### Why Fixed Size First?

* Deterministic
* Performant
* Good baseline
* Easy to test

---

### Why Overlap?

Naive chunking loses context at boundaries.

Example:

```
"...the cat sat on the mat. The mouse ran away."
```

Without overlap, both sentences might split.

With overlap, full context preserved.

---

### Why Separate Table?

Benefits:

* fast chunk lookup
* efficient filtering by document
* supports bulk operations
* prepares for vector storage

---

### Why Token Estimation?

Before embeddings/LLM:

```
Validate: char_count / 4 ≤ max_tokens

Execute with confidence
```

---

## How It Works

1. User uploads PDF.
2. Extraction creates raw text in `document_contents`.
3. ChunkingService loads raw text.
4. FixedSizeChunker splits into TextChunk objects.
5. Token metadata calculated.
6. DocumentChunk records created.
7. Stored in `document_chunks` table.
8. Indexed by document_id and chunk_index.

---

## Data Flow Example

**Upload:** `example.pdf`

↓

**Extraction:** 15,000 characters of raw text

↓

**Chunking (512 char chunks, 50 overlap):**

* Chunk 0: chars 0-512 (128 tokens est.)
* Chunk 1: chars 462-974 (128 tokens est.)
* Chunk 2: chars 924-1436 (128 tokens est.)
* ... (continues)

↓

**Storage:** 30 DocumentChunk records created

---

## Interface

### ChunkingService.chunk_document_content()

```
Input:  document_id, raw_text
Output: list[DocumentChunk]
```

Handles:

* validation
* chunking strategy selection
* persistence
* error handling

---

## Query Optimization

Retrieve chunks for a document:

```
SELECT * FROM document_chunks
WHERE document_id = ?
ORDER BY chunk_index ASC
```

Enables:

* sequential processing
* retrieval (top-k)
* context assembly

---

## Design Patterns Applied

1. **Strategy Pattern** - Supports multiple chunking algorithms
2. **Dependency Injection** - Service receives repository
3. **Data Transfer Object** - TextChunk carries chunking data
4. **Repository Pattern** - Isolates persistence

---

## Interview Explanation

> We implemented a chunking layer that splits large documents into fixed-size chunks with configurable overlap. By using the Strategy pattern, we can easily add semantic chunking (using embeddings) or language-specific approaches later without changing the orchestration logic. Storing chunks in a separate table allows efficient retrieval and prepares us for vector storage.

---

## What Day 5 Unlocks

Once chunking is complete:

```
Document Upload

↓

Text Extraction

↓

Chunk Creation

↓

Chunk Storage
```

This enables:

* **Day 6:** Embeddings generation
* **Day 7:** Vector database integration
* **Day 8:** Semantic search
* **Day 9:** RAG pipeline

---

## Milestone Achieved

Application can process documents into structured chunks ready for embeddings.

---

# Overall Progress

| Day   | Status                          |
| ----- | ------------------------------- |
| Day 1 | ✅ Complete                      |
| Day 2 | ✅ Complete                      |
| Day 3 | ✅ Complete                      |
| Day 4 | ✅ Complete                      |
| Day 5 | ✅ Complete                      |

---

# Lessons Learned So Far

1. Good architecture is more important than writing AI code quickly.
2. Separate responsibilities early.
3. Design for replacement (StorageService, ProcessorFactory, ChunkingStrategy).
4. Keep metadata separate from large content.
5. Introduce abstractions before complexity arrives.
6. Build production infrastructure first, AI capabilities second.
7. Chunking strategy is critical for retrieval quality—invest in the right approach for your domain.
8. Overlap between chunks prevents information loss at boundaries.
