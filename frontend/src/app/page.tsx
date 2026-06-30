"use client";

import { useCallback, useState, useEffect } from "react";

import BuildForm from "@/components/BuildForm";
import ProgressBar from "@/components/ProgressBar";
import usePolling from "@/hooks/usePolling";
import ProfileReview from "@/components/ProfileReview";

import { useSearchParams } from "next/navigation";
import { getSavedProfile } from "@/services/api";

export default function Home() {
  const [jobId, setJobId] = useState("");

  const [status, setStatus] = useState("");

  const [progress, setProgress] = useState(0);

  const [profile, setProfile] = useState<any>(null);

  const searchParams = useSearchParams();

  const [error, setError] = useState("");

  useEffect(() => {

    const savedJobId = searchParams.get("jobId");

    if (!savedJobId)
        return;

    const load = async () => {

        try {

            const response =
                await getSavedProfile(savedJobId);

            if (response.data?.profile_json) {

                setJobId(savedJobId);

                setProfile(response.data.profile_json);

            }

        } catch (error) {

            console.log(error);

        }

    };

    load();

  }, []);

  const updateStatus = useCallback((data: any) => {
    setStatus(data.status);
    setProgress(data.progress);
  
    if (data.status === "done") {
      setProfile(data.profile);
      setError("");
    }
  
    if (data.status === "failed") {
      setError(data.error);
    }
  }, []);

  usePolling({
    jobId,
    onUpdate: updateStatus,
  });

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-100">

      {!jobId && (
        <BuildForm onJobCreated={setJobId} />
      )}

      {jobId && !profile && !error && (
          <ProgressBar
              progress={progress}
              status={status}
          />
      )}

      {profile && (
        <div className="rounded-xl bg-white p-8 shadow-xl">

          <h2 className="mb-5 text-3xl font-bold">
            {profile && (
                <ProfileReview
                jobId={jobId}
                profile={profile}
                onHome={() => {
                    setJobId("");
                    setProfile(null);
                    setProgress(0);
                    setStatus("");
                    setError("");
                }}
            />
            )}
          </h2>

          <p>
            Total Fields:
            <strong>
              {" "}
              {profile.length}
            </strong>
          </p>

        </div>
      )}

      {error && (
          <div className="rounded-xl bg-white p-8 shadow-lg text-center">

              <h2 className="text-2xl font-bold text-red-600">
                  Build Failed
              </h2>

              <p className="mt-4">
                  {error}
              </p>

              <button
                  className="mt-6 rounded bg-blue-600 px-6 py-3 text-white"
                  onClick={() => {
                      setJobId("");
                      setProfile(null);
                      setProgress(0);
                      setStatus("");
                      setError("");
                  }}
              >
                  Retry
              </button>

          </div>
      )}

    </main>
  );
}