import axios from "axios";
import { ProfileField } from "@/types/profile";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const startBuild = (ticker: string) =>
  api.post("/build", { ticker });

export const getProfile = (jobId: string) =>
  api.get(`/profile/${jobId}`);

export const saveProfile = (
  jobId: string,
  profile: ProfileField[]
) =>
  api.post(`/profile/save/${jobId}`, profile);

export const getSavedProfile = (jobId: string) =>
  api.get(`/profile/saved/${jobId}`);

export default api;