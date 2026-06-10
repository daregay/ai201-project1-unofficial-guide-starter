# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- My project is an Unofficial Guide to Surviving CU Boulder. It covers the practical stuff that actually matters to students — orientation tips, study spaces, dining, getting around, campus resources, and things people wish someone had told them before they showed up.
The reason this is worth building is that the official CU Boulder website tells you what services exist, but it doesn't really tell you how to use them or what's actually worth your time. Reddit has that kind of honest advice, but it's all over the place and hard to search. This project pulls it together into something more useful. -->

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Boulder Colorado USA CU Student Guide | General guide for visiting and understanding CU Boulder | https://www.bouldercoloradousa.com/things-to-do/visiting-cu/cu-student-guide/ |
| 2 | CU Boulder Undergraduate Orientation | Official orientation information for new undergraduate students | https://www.colorado.edu/orientation/undergraduate-students |
| 3 | CU Boulder "I Wish I Had Known" | Student advice about things they wish they knew earlier | https://www.colorado.edu/orientation/i-wish-i-had-known |
| 4 | CU Boulder Exploring Boulder | Guide to exploring Boulder as a student | https://www.colorado.edu/studentlife/exploring-boulder |
| 5 | CU Boulder Transportation Options | Official transportation options for students | https://www.colorado.edu/pts/transportation-options |
| 6 | CU Boulder Today Getting Around Tips | Practical tips for getting around campus and Boulder | https://www.colorado.edu/today/2025/08/20/tips-getting-around-campus-and-boulder-ease |
| 7 | Reddit Campus Resource Thread | Students discuss campus resources they wish they knew about | https://www.reddit.com/r/cuboulder/comments/aj8bd8/what_was_a_campus_resource_you_wish_you_had_known/ |
| 8 | Reddit Before Enrolling Thread | Students share what they wish they knew before enrolling | https://www.reddit.com/r/cuboulder/comments/1bcof00/what_do_you_wish_you_knew_before_enrolling_at/ |
| 9 | Reddit Honest Opinions Thread | Current students and alumni share honest opinions about CU Boulder | https://www.reddit.com/r/cuboulder/comments/18iifhv/current_students_and_alumni_what_are_your_honest/ |
| 10 | Reddit Dining Thread | Students discuss C4C eating and dining recommendations | | 10 | Reddit Study Spaces Thread | Students discuss quiet and useful places to study on campus | https://www.reddit.com/r/cuboulder/comments/1bbs71n/study_spaces_that_are_actually_silent/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size: 700 characters**

**Overlap: 120 characters**

**Reasoning: **
My sources are a mix of official pages and Reddit threads, so the writing style varies a lot. Official pages tend to have longer, more structured paragraphs, while Reddit comments are short and scattered. A 700-character chunk is big enough to keep one complete idea together — like a single tip about transportation or a dining recommendation — without accidentally grouping unrelated things. The 120-character overlap is there so useful advice doesn't get cut in half at a chunk boundary. If a tip starts near the end of one chunk and keeps going into the next, the overlap gives the retriever a better shot at catching the whole thing.

## Retrieval Approach

**Embedding model:** sentence-transformers/all-MiniLM-L6-v2

**Top-k:** 5 chunks per query

**Production tradeoff reflection:**

I went with all-MiniLM-L6-v2 because it runs locally, it's free, and it's fast enough for a project at this scale. In a real production system, I'd want to compare multiple embedding models and evaluate retrieval accuracy, latency, cost, context length, and performance on informal student-written content. A larger model might perform better on Reddit-style language, slang, abbreviations, and nuanced student experiences, but it would also increase inference time and infrastructure costs. Those tradeoffs become much more important when serving real users at scale.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students wish they knew before enrolling at CU Boulder? | The system should pull from the "I Wish I Had Known" page and the Reddit thread, including advice about using campus resources early, preparing for the social side of college, and managing expectations before arriving. |
| 2 | What transportation options are available for CU Boulder students? | The system should cover buses, biking, walking, and parking resources from the official transportation pages. |
| 3 | What campus resources do students wish they had known about earlier? | The system should use the Reddit resource thread and surface resources students found most helpful or most overlooked. |
| 4 | What do students say about eating at C4C or campus dining? | The system should pull from the dining thread and provide a realistic summary of what students recommend or avoid. |
| 5 | What are students' honest opinions about CU Boulder? | The system should reflect both positive and negative perspectives from the honest opinions thread and make clear that these are student opinions rather than official university messaging. |

---

## Anticipated Challenges

1. Reddit threads can contain jokes, off-topic comments, repeated information, and low-quality responses. These noisy chunks may rank highly during retrieval and reduce answer quality.

2. Official CU Boulder pages often contain navigation menus, headers, footers, and boilerplate text mixed with the main content. Without proper cleaning, the retrieval system may return irrelevant page elements instead of useful information.

3. Some questions naturally require information from multiple sources. For example, a question about freshman advice may match both official orientation materials and several Reddit discussions. The generation step must combine information clearly while preserving source attribution.

---

## Architecture

```text
Raw Documents / URLs
        ↓
Document Ingestion
(load text from saved .txt files or copied webpage text)
        ↓
Cleaning
(remove navigation text, extra whitespace, ads, unrelated text)
        ↓
Chunking
(700-character chunks with 120-character overlap)
        ↓
Embedding
(sentence-transformers/all-MiniLM-L6-v2)
        ↓
Vector Store
(ChromaDB with source metadata)
        ↓
Retrieval
(top 5 chunks by semantic similarity)
        ↓
Generation
(Groq llama-3.3-70b-versatile answers only from retrieved context)
        ↓
User Interface
(simple query interface showing answer and sources)
```

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**

I'll use ChatGPT to help build the ingestion and chunking pipeline. I'll share the Domain, Documents, and Chunking Strategy sections and ask it to help write code that loads text files, strips out extra whitespace and irrelevant text, splits content into 700-character chunks with 120-character overlap, and preserves source metadata. To verify the implementation, I'll print at least five sample chunks and check that they are readable, contain complete ideas, and correctly retain their source information.

**Milestone 4 — Embedding and retrieval:**

I'll use ChatGPT to help set up the embedding and retrieval pipeline using sentence-transformers/all-MiniLM-L6-v2 and ChromaDB. I'll provide the Retrieval Approach and Architecture sections as input. The expected output is code that embeds each chunk, stores embeddings and metadata in ChromaDB, and retrieves the top five most relevant chunks for a user query. I'll verify the implementation by testing at least three questions from the Evaluation Plan and confirming that the retrieved chunks contain information relevant to the query.

**Milestone 5 — Generation and interface:**

I'll use ChatGPT to help write the generation prompt and build the user query interface. I'll provide the grounding requirements, Evaluation Plan, and Architecture sections. The expected output is a prompt and interface that answer questions using only retrieved context and display source information. I'll verify the system by testing questions that are covered by the documents and at least one question that is not covered, ensuring the model does not hallucinate information and instead states when the answer cannot be found in the retrieved text.I will design a prompt that instructs the Groq llama-3.3-70b-versatile model to answer only from retrieved chunks, cite sources, and respond that it does not have enough information when the answer is not present in the retrieved context.

---
