"use client";

import { useState } from "react";
import api from "@/services/api";

interface Props {
  onJobCreated: (jobId: string) => void;
}

export default function BuildForm({ onJobCreated }: Props) {
  const [ticker, setTicker] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    setError("");

    if (!ticker.trim()) {
      setError("Ticker is required.");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post("/build", {
        ticker,
      });

      onJobCreated(response.data.job_id);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          "Unable to start profile build."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-lg rounded-xl bg-white p-8 shadow-lg">

      <h2 className="mb-6 text-center text-3xl font-bold">
        Company Profile Builder
      </h2>

      <form
        onSubmit={handleSubmit}
        className="space-y-5"
      >
        <div>

          <label className="mb-2 block font-medium">
            Stock Ticker
          </label>

          <input
            type="text"
            value={ticker}
            onChange={(e) =>
              setTicker(e.target.value.toUpperCase())
            }
            placeholder="AAPL"
            className="w-full rounded-lg border p-3 outline-none focus:border-blue-500"
          />

        </div>

        {error && (
          <div className="rounded bg-red-100 p-3 text-red-600">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-blue-600 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading
            ? "Starting Build..."
            : "Build Company Profile"}
        </button>
      </form>

    </div>
  );
}