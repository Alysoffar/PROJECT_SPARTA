import axios, { AxiosInstance } from 'axios';
import { WorkflowRequest, WorkflowStatus, WorkflowResult } from '../types/api';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api/v1`,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async createWorkflow(request: WorkflowRequest): Promise<WorkflowStatus> {
    const response = await this.client.post<WorkflowStatus>('/workflows', request);
    return response.data;
  }

  async getWorkflowStatus(workflowId: string): Promise<WorkflowStatus> {
    const response = await this.client.get<WorkflowStatus>(`/workflows/${workflowId}`);
    return response.data;
  }

  async getWorkflowResult(workflowId: string): Promise<WorkflowResult> {
    const response = await this.client.get<WorkflowResult>(`/workflows/${workflowId}/result`);
    return response.data;
  }

  async cancelWorkflow(workflowId: string): Promise<void> {
    await this.client.delete(`/workflows/${workflowId}`);
  }
}

export const apiClient = new ApiClient();
