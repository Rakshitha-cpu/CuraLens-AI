// Safely converts any value coming from the Gemini/backend JSON into
// something React can render as text.
//
// Why this exists: Gemini's JSON output is not always shaped the way the
// UI expects. A field like `medicine.name` or `safety.overall_risk` is
// usually a string, but it can come back as an object (e.g.
// { value: "Paracetamol", confidence: 0.9 }), a boolean, or an array of
// mixed types. Rendering any non-primitive directly in JSX ({value})
// throws "Objects are not valid as a React child" and crashes the whole
// Dashboard. This function normalizes all of those cases into a string
// (or a fallback) so a single malformed field never takes down the page.
export function renderValue(value, fallback = "Not Available") {
  if (value === null || value === undefined) return fallback;

  if (typeof value === "string") {
    return value.trim() !== "" && value !== "UNKNOWN" ? value : fallback;
  }

  if (typeof value === "number") return value;

  if (typeof value === "boolean") return value ? "Yes" : "No";

  if (Array.isArray(value)) {
    const parts = value
      .map((item) => renderValue(item, ""))
      .filter((item) => item !== "" && item !== fallback);
    return parts.length ? parts.join(", ") : fallback;
  }

  if (typeof value === "object") {
    // Common shapes Gemini/LLM JSON tends to use for a "labelled" value.
    const preferredKeys = ["value", "text", "name", "label", "description", "summary"];
    for (const key of preferredKeys) {
      if (value[key] !== undefined) return renderValue(value[key], fallback);
    }
    // Last resort: stitch together any primitive fields found on the object
    // rather than crashing or showing "[object Object]".
    const parts = Object.values(value).filter(
      (v) => typeof v === "string" || typeof v === "number"
    );
    return parts.length ? parts.join(", ") : fallback;
  }

  return String(value);
}
