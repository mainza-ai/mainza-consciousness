import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs))
}

/**
 * Parses a plain text message from a structured agent response.
 * Agents can return complex objects (JSON, stringified JSON, etc.).
 * This function extracts the primary human-readable message.
 *
 * @param response The raw response from the agent endpoint.
 * @returns A plain text string for display or TTS.
 */
export function parseAgentResponse(response: any): string {
  if (!response) {
    return "Error: Received an empty response.";
  }

  // If response has a primary 'answer' field (e.g., from RAG agent)
  if (typeof response === 'object' && response.answer) {
    // If the answer itself is a stringified object, recursively parse it
    if (typeof response.answer === 'string' && /answer=(["'])([\s\S]+?)\1/.test(response.answer)) {
      return parseAgentResponse(response.answer);
    }
    return response.answer;
  }

  // If response is a string that looks like "context=[] chunks=[] answer='...'"
  if (typeof response === 'string') {
    // Try to extract answer='...' using a non-greedy regex that matches across newlines and both quote types
    const match = response.match(/answer=(["'])([\s\S]+?)\1/);
    if (match) {
      console.debug('[parseAgentResponse] Extracted answer:', match[2]);
      return match[2];
    }
    // Try to parse as JSON
    try {
      const parsed = JSON.parse(response);
      return parseAgentResponse(parsed);
    } catch (e) {
      // It's just a regular string.
      return response;
    }
  }

  // If response has a primary 'summary' field (e.g., from GraphMaster summarize)
  if (typeof response === 'object' && response.summary) {
    return response.summary;
  }

  // If response has a 'result' field which might contain the text
  if (typeof response === 'object' && response.result) {
    // If result is an array, it might be from a direct Cypher query.
    // We'll format it lightly.
    if (Array.isArray(response.result)) {
      if (response.result.length === 0) {
        return "Query executed successfully, but returned no results.";
      }
      // Attempt to find a 'summary' or 'name' or 'text' field in the first result item
      const firstResult = response.result[0];
      if (typeof firstResult === 'object') {
        if (firstResult.summary) return firstResult.summary;
        if (firstResult.text) return firstResult.text;
        if (firstResult.name) return `Found entity: ${firstResult.name}`;
      }
      return `Query returned ${response.result.length} results. View the console for details.`;
    }
    // If result is a string, return it directly.
    if (typeof response.result === 'string') {
      return response.result;
    }
  }

  // Fallback for other object structures: stringify the object.
  // This is the "user should not see JSON" failsafe.
  // We return a generic message and log the object for debugging.
  console.warn("Could not parse agent response:", response);
  return "Received a complex object. Check the console for the full response.";
}
