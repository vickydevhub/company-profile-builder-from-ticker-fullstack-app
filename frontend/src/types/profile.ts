export interface BuildResponse {
    job_id: string;
  }
  
  export interface Candidate {
    value: string;
    source: string;
    source_url: string;
    confidence: number;
  }
  
  export interface ProfileField {
    section: string;
    field: string;
    label: string;
  
    value?: string | null;
  
    source?: string;
    source_url?: string;
    source_date?: string;
  
    confidence?: number;
  
    note?: string;
  
    conflict?: boolean;
  
    candidates?: Candidate[];
  
    // UI state
    accepted?: boolean;
    rejected?: boolean;
    editedValue?: string;
  }
  
  export interface ProfileResponse {
    status: "running" | "done" | "failed";
  
    progress: number;
  
    profile?: ProfileField[];
  
    error?: string;
  }