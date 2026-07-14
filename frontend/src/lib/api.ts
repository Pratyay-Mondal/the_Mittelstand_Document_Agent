const API_BASE = "http://localhost:8000/api";

export async function uploadPdf(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload document");
  }

  return response.json();
}

export async function getOriginalExtraction(docId: string) {
  const response = await fetch(`${API_BASE}/extraction/${docId}`);
  if (!response.ok) {
    throw new Error("Failed to load extraction");
  }
  return response.json();
}

export async function updateExtraction(docId: string, extractionData: any) {
  const response = await fetch(`${API_BASE}/extraction/${docId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(extractionData),
  });

  if (!response.ok) {
    throw new Error("Failed to save extraction");
  }

  return response.json();
}

export async function reExtract(docId: string) {
  const response = await fetch(`${API_BASE}/extraction/${docId}/re-extract`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to trigger re-extraction");
  }

  return response.json();
}

export const getStreamUrl = (docId: string, question: string) => {
  return `${API_BASE}/chat/stream?doc_id=${docId}&question=${encodeURIComponent(question)}`;
};
