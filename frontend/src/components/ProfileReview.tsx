"use client";

import { useState } from "react";

import { ProfileField } from "@/types/profile";
import FieldCard from "./FieldCard";
import ConflictField from "./ConflictField";
import { saveProfile } from "@/services/api";
import { useRouter } from "next/navigation";

interface Props {
  jobId: string;
  profile: ProfileField[];
  onHome: () => void;
}

export default function ProfileReview({ jobId, profile, onHome }: Props) {
  const [reviewedFields, setReviewedFields] =
    useState<ProfileField[]>(profile);
  
  const [saving, setSaving] = useState(false);

  const router = useRouter();

  const updateField = (
    fieldName: string,
    updatedField: ProfileField
  ) => {
    setReviewedFields((prev) =>
      prev.map((field) =>
        field.field === fieldName ? updatedField : field
      )
    );
  };

  // Bulk Accept
  const acceptAll = () => {
    setReviewedFields((prev) =>
      prev.map((field) => ({
        ...field,
        accepted: true,
        rejected: false,
      }))
    );
  };

  // Bulk Reject
  const rejectAll = () => {
    setReviewedFields((prev) =>
      prev.map((field) => ({
        ...field,
        accepted: false,
        rejected: true,
      }))
    );
  };

  // Accept only high confidence fields
  const acceptHighConfidence = () => {
    setReviewedFields((prev) =>
      prev.map((field) => {
        if (
          field.conflict ||
          field.confidence === undefined ||
          field.confidence < 0.6
        ) {
          return field;
        }

        return {
          ...field,
          accepted: true,
          rejected: false,
        };
      })
    );
  };

  const grouped = reviewedFields.reduce(
    (acc: Record<string, ProfileField[]>, item) => {
      if (!acc[item.section]) {
        acc[item.section] = [];
      }

      acc[item.section].push(item);

      return acc;
    },
    {}
  );

  const acceptedCount = reviewedFields.filter(
    (field) => field.accepted
  ).length;

  const handleSave = async () => {
    try {
      setSaving(true);
  
      await saveProfile(jobId, reviewedFields);
  
      window.history.replaceState(
        {},
          "",
          `/?jobId=${jobId}`
      );
  
    } catch (error) {
      alert("Unable to save profile.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="mx-auto max-w-6xl space-y-8">

      <div className="rounded-xl bg-white p-5 shadow">

        <div className="flex flex-wrap items-center justify-between gap-4">

          <div>
            <h1 className="text-3xl font-bold">
              Review Company Profile
            </h1>

            <p className="mt-2 text-gray-600">
              Accepted {acceptedCount} / {reviewedFields.length}
            </p>
          </div>

          <div className="flex flex-wrap gap-2">

            <button
              onClick={acceptHighConfidence}
              className="rounded bg-blue-600 px-4 py-2 text-white"
            >
              Accept High Confidence
            </button>

            <button
              onClick={acceptAll}
              className="rounded bg-green-600 px-4 py-2 text-white"
            >
              Accept All
            </button>

            <button
              onClick={rejectAll}
              className="rounded bg-red-600 px-4 py-2 text-white"
            >
              Reject All
            </button>

          </div>

        </div>

      </div>

      {Object.entries(grouped).map(([section, fields]) => (

        <div key={section}>

          <h2 className="mb-4 border-b pb-2 text-2xl font-bold">
            {section}
          </h2>

          <div className="space-y-4">

            {fields.map((field) =>
              field.conflict ? (
                <ConflictField
                  key={field.field}
                  field={field}
                  onUpdate={updateField}
                />
              ) : (
                <FieldCard
                  key={field.field}
                  field={field}
                  onUpdate={updateField}
                />
              )
            )}

          </div>

        </div>

      ))}
      <div className="flex justify-center pt-8">

      <button
          onClick={handleSave}
          disabled={saving}
          className="rounded-lg bg-indigo-600 px-8 py-3 text-white hover:bg-indigo-700 disabled:bg-gray-400"
      >

          {saving
              ? "Saving..."
              : "Save Profile"}

      </button>
      <button
           onClick={onHome}
          className="rounded bg-gray-700 px-4 py-2 text-white hover:bg-gray-800"
      >
          🏠 Home
      </button>
      </div>
    </div>
  );
}