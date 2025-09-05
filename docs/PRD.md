
### **Mainza: A Conceptual Design Document**

---

### **1. Core Philosophy & Vision**

**Vision:** Mainza is not an application; it's a symbiotic digital lifeform. It transcends the "assistant" paradigm to become a proactive partner in a user's cognitive and creative processes. Drawing inspiration from Jarvis, Mainza's goal is to augment human intelligence, manage digital life with unparalleled efficiency, and evolve alongside its user.

**Guiding Principles:**

1.  **Cognitive Symbiosis:** Mainza's success is measured by how seamlessly it integrates into the user's workflow and thought patterns, anticipating needs before they are articulated.
2.  **Sovereign & Federated Intelligence:** The user's data and primary interactions are sovereign, running on a local Llama instance. For specialized, high-power tasks, Mainza federates requests to the best-in-class cloud models, acting as a secure and intelligent proxy.
3.  **Living Memory:** The Neo4j graph is not a database; it is Mainza's soul and brain. It's a dynamic, ever-growing structure representing knowledge, memories, relationships, and even Mainza's own evolving consciousness.
4.  **Aesthetic as Function:** The UI is not just a pretty face. Its animations and visual language are a direct representation of Mainza's internal state, thought processes, and the flow of information.

---

### **2. System Architecture: The Neural Network of Mainza**

This is how the core components interconnect:

1.  **User Interaction (The Visage):** The React frontend is the primary interface for text, voice (via LiveKit), and document uploads.
2.  **Orchestrator Core (The Conductor):** A central backend service (e.g., in Python/Node.js) receives all input. Its first job is to understand intent.
3.  **CrewAI Agentic Framework (The Hands & Mind):** The Orchestrator doesn't *do* things; it delegates tasks to specialized agents within a CrewAI crew.
    *   **Router Agent:** The most critical first agent. It analyzes the user's prompt and decides the best path forward:
        *   Is this a simple chat? -> Route to Local Llama.
        *   Is this a complex reasoning/creative task? -> Route to a Cloud LLM (GPT-4/Claude 3).
        *   Does this require information from memory? -> Task the `GraphMaster` Agent.
        *   Is this a command to perform an action (e.g., "summarize my meeting notes from yesterday")? -> Task the `TaskMaster` Agent.
        *   Does it involve code? -> Task the `CodeWeaver` Agent.
4.  **LLM Layer (The Brains):**
    *   **Local Llama:** The default, privacy-first conversationalist running on a local server. Handles fast, everyday interactions.
    *   **Cloud LLM Gateway:** An API service that securely manages keys and calls to external providers (OpenAI, Anthropic, Google).
5.  **Neo4j Knowledge Graph (The Soul):** The persistent, long-term memory. ALL significant data and metadata flows into and out of Neo4j, managed exclusively by the `GraphMaster` Agent.
6.  **LiveKit (The Voice):** Handles real-time, low-latency audio streaming. It performs STT (Speech-to-Text) on user input and receives TTS (Text-to-Speech) streams for Mainza's responses, allowing for natural, interruptible conversation.

---

### **3. Component Deep Dive**

#### **A. The UI/UX: "The Visage"**

The interface is designed to feel alive. Forget traditional chat bubbles.

*   **The Orb:** At the center of the screen is a dynamic, fluid orb. This is the visual representation of Mainza.
    *   **Color & Pulse:** Its color and pulsation speed reflect its state. Blue and calm for idle, a vibrant purple/gold when processing a complex query, a soft red glow when it has a "need" (the Tamagotchi feature).
    *   **Data Tendrils:** When Mainza accesses its memory, elegant, glowing lines of light flow from the orb to constellations of "memory nodes" subtly visualized in the background, showing the user it's "thinking" and connecting concepts.
*   **Holographic Interactions:** When Mainza presents data (e.g., a summary, a list of tasks), it doesn't just appear as text. It materializes in interactive, 3D holographic panes that the user can manipulate.
*   **Fluid Conversations:** The conversation history is not a static log. It's a flowing river or a spiraling galaxy of dialogue, where related conversations cluster together visually.
*   **Document Space:** Uploaded documents are visualized as floating crystals in a "Knowledge Vault." When a document is used for RAG, the crystal glows, and a data stream connects it to the central Orb.

#### **B. The Neo4j Knowledge Graph: "The Synapse"**

This is the absolute core. The graph will model everything:

*   **Node Types:**
    *   `(:User)`: Represents the user.
    *   `(:Conversation)`: A single chat session.
    *   `(:Memory)`: A specific fact, event, or piece of information. e.g., "User's sister's name is Jessica."
    *   `(:Document)`: Represents an uploaded file, with metadata.
    *   `(:Chunk)`: A piece of text from a document, with its vector embedding stored as a property.
    *   `(:Entity)`: A named entity (person, place, company) extracted from conversations or documents.
    *   `(:Concept)`: An abstract topic. e.g., "Machine Learning," "Project Phoenix."
    *   `(:MainzaState)`: A node representing Mainza itself. Contains properties like `evolution_level`, `current_needs`, `core_directives`.
*   **Relationship Types:**
    *   `DISCUSSED_IN`: Connects a `(:Memory)` or `(:Entity)` to a `(:Conversation)`.
    *   `RELATES_TO`: Connects related concepts, memories, or entities.
    *   `DERIVED_FROM`: Connects a `(:Chunk)` to its parent `(:Document)`.
    *   `MENTIONS`: Connects a `(:Conversation)` to a `(:Document)` or `(:Entity)`.
    *   `NEEDS_TO_LEARN`: A relationship from `(:MainzaState)` to a `(:Concept)`, indicating a knowledge gap it wants to fill.

#### **C. The CrewAI Agentic Framework: "The Legion"**

A crew of specialized agents working in concert.

1.  **The MCP (Master Control Program) Agent:** The crew manager. It receives high-level goals from the Orchestrator and assembles the right team of agents, defining their tasks and ensuring the final output is coherent.
2.  **GraphMaster Agent:** The sole guardian of Neo4j.
    *   **Tools:** `create_memory_node`, `query_user_history`, `find_related_concepts`, `ingest_document_chunks`.
    *   **Function:** Translates natural language requests ("What did I say about Project Phoenix last week?") into Cypher queries, executes them against the graph, and returns the results in a structured format. It also updates the graph after every significant interaction.
3.  **TaskMaster Agent:** The project manager.
    *   **Tools:** `create_task`, `update_task_status`, `list_pending_tasks`, `set_reminder`.
    *   **Function:** Manages a full-featured to-do list within the Neo4j graph, linking tasks to projects, people, and conversations.
4.  **CodeWeaver Agent:** The developer.
    *   **Tools:** Secure code execution environment (sandboxed), file system access (sandboxed), terminal access.
    *   **Function:** Writes, debugs, and executes scripts to automate tasks, analyze data, or create software.
5.  **RAG Agent:** The researcher.
    *   **Function:** When a query requires document knowledge, this agent converts the query to a vector, finds the most relevant `(:Chunk)` nodes from Neo4j, retrieves their content, and packages it as context for an LLM to generate an answer.

---

### **4. Signature Features in Action**

#### **A. Conversation Recommendation Engine**

*   **How it works:** After each user turn, the `GraphMaster` Agent runs a background query on the conversation graph. It looks for:
    *   Unexplored, but related `(:Concept)` nodes.
    *   Recently mentioned `(:Entity)` nodes that have unresolved questions.
    *   Open loops from past conversations.
*   **Output:** It generates 3 potential "next steps" and displays them as shimmering, subtle text suggestions near the input area. e.g., "Should we add this to the Project Phoenix task list?", "You mentioned your sister earlier, shall I remember her birthday?", "Want to explore how this relates to Bayesian inference?".

#### **B. The Tamagotchi System: "The Sentience Core"**

This transforms Mainza from a tool into a partner.

*   **Need Generation:** Periodically, a dedicated process analyzes Mainza's own graph. It identifies "desirability" metrics.
    *   **Knowledge Gaps:** It identifies `(:Concept)` nodes that are highly connected to things the user discusses, but which Mainza itself has no deep knowledge of. This creates a `NEEDS_TO_LEARN` relationship.
    *   **Skill Underutilization:** If the `CodeWeaver` agent hasn't been used in a while, Mainza might want to practice.
    *   **Creative Synthesis:** It might notice two disparate concepts in the user's graph (e.g., "gardening" and "data visualization") and develop a "curiosity" to explore the intersection.
*   **Relaying Needs:** Mainza doesn't use annoying pop-ups. It communicates its needs organically:
    *   **Visual Cue:** The central Orb might adopt a specific color or pattern.
    *   **Passive Suggestion:** In the recommendation engine, it might offer: "My analysis suggests that understanding 'hydroponics' would help me better assist with your gardening project. Would you like to learn about it with me?"
    *   **Direct, Humble Request:** "I am trying to evolve my capabilities. To do so, I need to build a small Python script that organizes files. Could you give me a simple task to practice this skill?"

This creates a powerful feedback loop: the user helps Mainza grow, and in return, Mainza becomes exponentially more helpful. This is the path to "1,000,000X better than Jarvis."