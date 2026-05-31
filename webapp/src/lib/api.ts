/**
 * Base URL for the backend API.
 * Uses the environment variable, defaulting to localhost:8000 if not set.
 */
const getApiUrl = (): string => {
  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    // Only use local IP routing if we are accessing a local IP address (e.g. 10.68.220.252)
    const isIpAddress = /^(\d{1,3}\.){3}\d{1,3}$/.test(hostname);
    if (isIpAddress) {
      return `http://${hostname}:8000`;
    }
  }
  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
};

const API_URL = getApiUrl();

/**
 * A generalized API client to make requests to the backend.
 * Automatically handles JSON parsing, error throwing, and base URL prefixing.
 */
export const apiClient = {
  /**
   * Make a GET request
   * @param endpoint The path (e.g., "/analyze")
   * @param headers Optional custom headers
   */
  async get<T>(endpoint: string, headers: HeadersInit = {}): Promise<T> {
    const url = `${API_URL}${endpoint}`;
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const detailMsg = errorData?.detail || errorData?.message;
      throw new Error(detailMsg || `GET request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  },

  /**
   * Make a POST request
   * @param endpoint The path
   * @param body The body to send
   * @param headers Optional custom headers
   */
  async post<T>(endpoint: string, body: any, headers: HeadersInit = {}): Promise<T> {
    const url = `${API_URL}${endpoint}`;
    
    // Check if the body is FormData (e.g., for file uploads)
    const isFormData = body instanceof FormData;
    
    const fetchHeaders: HeadersInit = { ...headers };
    
    // Do not set Content-Type if sending FormData, the browser will set it with the correct boundary
    if (!isFormData) {
      (fetchHeaders as Record<string, string>)["Content-Type"] = "application/json";
      body = JSON.stringify(body);
    }

    const response = await fetch(url, {
      method: "POST",
      headers: fetchHeaders,
      body,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const detailMsg = errorData?.detail || errorData?.message;
      throw new Error(detailMsg || `POST request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  },
};
