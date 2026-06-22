import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
});

api.interceptors.request.use((config: AxiosRequestConfig) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`,
    };
  }
  return config;
});

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const login = (data: LoginRequest): Promise<AxiosResponse<LoginResponse>> => {
  return api.post('/api/auth/login', data);
};

export interface RegisterRequest {
  username: string;
  password: string;
  email: string;
}

export interface RegisterResponse {
  id: number;
  username: string;
  email: string;
}

export const register = (data: RegisterRequest): Promise<AxiosResponse<RegisterResponse>> => {
  return api.post('/api/auth/register', data);
};

export const logout = (): Promise<AxiosResponse<void>> => {
  return api.post('/api/auth/logout');
};

export interface Document {
  id: number;
  name: string;
  uploaded_at: string;
}

export const getDocuments = (): Promise<AxiosResponse<Document[]>> => {
  return api.get('/api/documents');
};

export interface UploadDocumentRequest {
  file: File;
}

export interface UploadDocumentResponse {
  id: number;
  name: string;
  uploaded_at: string;
}

export const uploadDocument = (data: FormData): Promise<AxiosResponse<UploadDocumentResponse>> => {
  return api.post('/api/documents/upload', data, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export interface IngestDocumentsResponse {
  success: boolean;
  message: string;
}

export const ingestDocuments = (): Promise<AxiosResponse<IngestDocumentsResponse>> => {
  return api.post('/api/ai/ingest');
};

export interface AIQueryRequest {
  query: string;
  top_k: number;
}

export interface AIQueryResponse {
  answer: string;
  sources: Array<{
    id: number;
    content: string;
    relevance: number;
  }>;
}

export const aiQuery = (data: AIQueryRequest): Promise<AxiosResponse<AIQueryResponse>> => {
  return api.post('/api/ai/query', data);
};