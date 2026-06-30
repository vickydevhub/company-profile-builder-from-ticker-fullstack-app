"use client";

import { useEffect } from "react";
import api from "@/services/api";

interface Props {
  jobId: string;
  onUpdate: (data: any) => void;
}

export default function usePolling({
  jobId,
  onUpdate,
}: Props) {
  useEffect(() => {
    if (!jobId) return;

    const interval = setInterval(async () => {
      try {
        const response = await api.get(
          `/profile/${jobId}`
        );

        onUpdate(response.data);

        if (
          response.data.status === "done" ||
          response.data.status === "failed"
        ) {
          clearInterval(interval);
        }
      } catch (error) {
        console.error(error);
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId, onUpdate]);
}