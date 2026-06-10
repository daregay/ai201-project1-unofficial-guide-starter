# The Unofficial Guide — Project 1

## Domain

The Unofficial Guide to Surviving CU Boulder is a retrieval-augmented generation (RAG) system that helps students find practical information about student life at the University of Colorado Boulder. The system covers topics such as orientation, study spaces, dining, transportation, campus resources, and advice from current students and alumni.

This knowledge is valuable because official university websites explain what services exist, but they often do not capture student experiences, recommendations, or practical advice. Many of these insights are scattered across Reddit discussions and difficult to search efficiently. This project combines official information and student perspectives into a single searchable system.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | CU Student Guide | Official Website | https://www.bouldercoloradousa.com/things-to-do/visiting-cu/cu-student-guide/ |
| 2 | Undergraduate Orientation | Official Website | https://www.colorado.edu/orientation/undergraduate-students |
| 3 | I Wish I Had Known | Official Website | https://www.colorado.edu/orientation/i-wish-i-had-known |
| 4 | Exploring Boulder | Official Website | https://www.colorado.edu/studentlife/exploring-boulder |
| 5 | Transportation Options | Official Website | https://www.colorado.edu/pts/transportation-options |
| 6 | Getting Around Campus and Boulder with Ease | Official Website | https://www.colorado.edu/today/2025/08/20/tips-getting-around-campus-and-boulder-ease |
| 7 | Campus Resources Students Wish They Knew About | Reddit Thread | https://www.reddit.com/r/cuboulder/comments/aj8bd8/what_was_a_campus_resource_you_wish_you_had_known/ |
| 8 | What Do You Wish You Knew Before Enrolling at CU Boulder? | Reddit Thread | https://www.reddit.com/r/cuboulder/comments/1bcof00/what_do_you_wish_you_knew_before_enrolling_at/ |
| 9 | Honest Opinions About CU Boulder | Reddit Thread | https://www.reddit.com/r/cuboulder/comments/18iifhv/current_students_and_alumni_what_are_your_honest/ |
| 10 | Study Spaces That Are Actually Silent | Reddit Thread | https://www.reddit.com/r/cuboulder/comments/1bbs71n/study_spaces_that_are_actually_silent/ |
| 11 | Recommendations for C4C Eating | Reddit Thread | https://www.reddit.com/r/cuboulder/comments/1obrd8v/recommendations_for_c4c_eating/ |

---

## Chunking Strategy

**Chunk size:** 700 characters

**Overlap:** 120 characters

**Why these choices fit your documents:**

The document collection contains a mixture of official university pages and Reddit discussions. Official pages contain longer paragraphs and structured information, while Reddit threads contain shorter comments and conversational text. A chunk size of 700 characters was chosen to preserve complete ideas without combining unrelated topics. An overlap of 120 characters helps prevent useful information from being split across chunk boundaries and improves retrieval quality when relevant information appears near the edge of a chunk.

Before chunking, documents were cleaned by removing extra whitespace, empty lines, and common navigation text. The final corpus contained 73 chunks across 11 documents.

**Final chunk count:** 73

---

## Embedding Model

**Model used:** sentence-transformers/all-MiniLM-L6-v2

**Production tradeoff reflection:**

I selected all-MiniLM-L6-v2 because it is free, runs locally, and provides strong semantic search performance for a project of this size. If cost were not a constraint, I would compare larger embedding models that may provide better retrieval accuracy on informal student-written content and longer documents. I would evaluate tradeoffs including retrieval accuracy, latency, multilingual support, context length, infrastructure cost, and whether the model should run locally or through a hosted API.

---

## Grounded Generation

**System prompt grounding instruction:**

The system prompt instructs the model to answer only from the retrieved context, avoid outside knowledge, avoid guessing, and refuse questions that are not supported by the retrieved documents. The prompt specifically tells the model to respond with:

> "I do not have enough information in the provided documents to answer that."

when sufficient evidence is not available.

**How source attribution is surfaced in the response:**

The retrieval system displays the source filename, chunk number, and similarity distance for all retrieved chunks. The generated answer also references the source documents used to construct the response. This allows users to trace answers back to the original documents and verify where the information came from.

---

## Failure Case Analysis

**Question that failed:**

What campus resources do students wish they had known about earlier?

**What the system returned:**

"I do not have enough information in the provided documents to answer that."

**Root cause (tied to a specific pipeline stage):**

The information existed within the corpus, but the retrieval stage failed to return the most relevant chunks from the `campus_resources_reddit.txt` document. Because the grounding prompt prevented the language model from using outside knowledge, the model correctly refused to answer rather than hallucinating information. This indicates a retrieval failure rather than a generation failure.

**What you would change to fix it:**

I would experiment with larger embedding models, increase the retrieval top-k value, improve chunking around resource-related discussions, and add metadata filtering to improve retrieval accuracy for specific campus resource questions.

---

## Spec Reflection

**One way the spec helped you during implementation:**

The planning document helped structure the project before implementation began. Defining the domain, document sources, chunking strategy, evaluation questions, and architecture upfront made it easier to build the ingestion, retrieval, and generation components without constantly changing direction. The evaluation plan also provided clear test cases that could be used to verify whether retrieval and generation were working as expected.

**One way your implementation diverged from the spec, and why:**

The original plan assumed that all evaluation questions would retrieve relevant information successfully. During testing, one evaluation question failed because the retrieval stage did not surface the most relevant chunks from the document collection. Instead of modifying the evaluation or changing the question, I documented the failure and analyzed its cause because understanding retrieval weaknesses is an important part of evaluating a RAG system. This made the final evaluation more realistic and highlighted areas for future improvement.



---

## Sample Chunks

### Sample Chunk 1

**Source:** honest_opinions_reddit.txt  
**Chunk index:** 0

```text
TITLE:
Current Students and Alumni: Honest Opinions About CU Boulder

A prospective transfer student asked current students and alumni for their honest opinions about attending CU Boulder. The discussion focused on academics, cost of living, student life, mental health support, transfer experiences, and career opportunities.
```

### Sample Chunk 2

**Source:** cu_student_guide.txt  
**Chunk index:** 0

```text
TITLE:
CU Student Guide to Boulder

Welcome to Boulder and the University of Colorado community. This guide introduces new students to some of the most popular places, activities, and experiences available in Boulder. Students are encouraged to explore the city, enjoy the outdoors, participate in community activities, and take advantage of opportunities.
```

### Sample Chunk 3

**Source:** getting_around_tips.txt  
**Chunk index:** 0

```text
TITLE:
Tips for Getting Around Campus and Boulder with Ease

CU Boulder offers a variety of transportation options that help students travel around campus and throughout Boulder. Students are encouraged to consider sustainable transportation methods such as biking, public transit, walking, and shared transportation services.
```

### Sample Chunk 4

**Source:** study_spaces_reddit.txt  
**Chunk index:** 0

```text
TITLE:
Study Spaces That Are Actually Silent

A student asked for recommendations for genuinely quiet study spaces on campus. Students discussed locations that tend to have minimal conversation, limited foot traffic, and quieter environments for focused studying.
```

### Sample Chunk 5

**Source:** dining_reddit.txt  
**Chunk index:** 0

```text
TITLE:
Student Recommendations for Dining Halls and Eating at CU Boulder

CU Boulder students discussed their favorite dining locations on campus and shared recommendations for avoiding crowds at dining halls. The discussion focused on dining hall quality, food options, and strategies for finding less crowded meal times.
```

---

## Example Responses

### Example Response 1

**Question:**  
Where are quiet places to study on campus?

**Response:**

Students commonly recommend the Engineering Center, Wolf Law Library, Math Library basement, Ketchum Building, Benson Library, and empty classrooms during evening hours. These locations were identified by students as some of the quietest places on campus for focused studying.

**Sources:**

- study_spaces_reddit.txt

### Example Response 2

**Question:**  
What transportation options are available for CU Boulder students?

**Response:**

CU Boulder students can use public transit, campus shuttles, biking, walking, carpooling, rideshare programs, scooters, skateboards, vanpools, e-bikes, NightRide services, and the CU Ski Bus. The university encourages sustainable transportation options whenever possible.

**Sources:**

- transportation_options.txt
- getting_around_tips.txt

### Out-of-Scope Example

**Question:**  
Who is the best computer science professor at CU Boulder?

**Response:**

> I do not have enough information in the provided documents to answer that.

---

## Query Interface

The system uses a Gradio web interface.

**Input:**  
A natural-language question about CU Boulder student life, transportation, dining, study spaces, or student experiences.

**Output:**  
A grounded answer generated from retrieved documents, along with source filenames, chunk identifiers, and similarity scores for the retrieved chunks.

### Example Interaction

**Question:**  
Where are quiet places to study on campus?

**Answer:**  
Engineering Center, Wolf Law Library, Math Library basement, Ketchum Building, Benson Library, and empty classrooms were commonly recommended by students as quiet study locations.

**Sources:**

- study_spaces_reddit.txt



---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students wish they knew before enrolling at CU Boulder? | Students mention academics, life skills, housing costs, time management, and preparing for independent living. | The system summarized academic preparation, personal responsibility, life skills, and Boulder housing costs. | Relevant | Accurate |
| 2 | What transportation options are available for CU Boulder students? | Students can use buses, shuttles, biking, walking, carpooling, rideshare programs, scooters, and other transportation services. | The system listed public transit, campus shuttles, biking, walking, carpooling, rideshare programs, scooters, skateboards, vanpools, e-bikes, NightRide, and the CU Ski Bus. | Relevant | Accurate |
| 3 | What campus resources do students wish they had known about earlier? | The system should identify resources students discussed in the campus resources Reddit thread. | The system responded that it did not have enough information in the provided documents to answer the question. | Off-target | Inaccurate |
| 4 | What do students say about eating at C4C or campus dining? | Students discuss crowd levels, food variety, favorite food stations, and dining recommendations. | The system reported that students like the food variety, recommended avoiding peak meal times, and highlighted several popular food options. | Relevant | Accurate |
| 5 | What are students' honest opinions about CU Boulder? | Students mention high housing costs but generally positive experiences, opportunities, and campus life. | The system summarized both positive and negative opinions, including housing costs, student opportunities, and overall quality of life. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target

**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My planned chunking strategy, including a 700-character chunk size and 120-character overlap.

- *What it produced:* Example chunking logic and recommendations for implementing the chunking function.

- *What I changed or overrode:* I verified that the implementation matched my planned chunk size and overlap values rather than accepting different values suggested during discussion. I also kept source metadata attached to every chunk because it was required for source attribution.

**Instance 2**

- *What I gave the AI:* The project requirements for retrieval, grounding, and evaluation, along with sample retrieval outputs from ChromaDB.

- *What it produced:* Suggestions for implementing semantic search, creating a grounded prompt, and formatting source citations.

- *What I changed or overrode:* I modified the grounding prompt to explicitly refuse questions that were not supported by retrieved documents. I also ensured that retrieved chunk information remained visible in the interface so users could inspect the evidence used to generate answers.


