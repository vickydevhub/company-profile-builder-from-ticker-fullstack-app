"use client";

import { useEffect, useState } from "react";

import { ProfileField } from "@/types/profile";

interface Props {
  field: ProfileField;
  onUpdate: (
    fieldName: string,
    field: ProfileField
  ) => void;
}

export default function FieldCard({
  field,
  onUpdate,
}: Props) {
  const [value, setValue] = useState(field.value ?? "");

  const [accepted, setAccepted] = useState(false);

  const [rejected, setRejected] = useState(false);

  useEffect(() => {
    onUpdate(field.field, {
      ...field,
      value,
      accepted,
      rejected,
    });
  }, [value, accepted, rejected]);

  const lowConfidence =
    field.confidence !== undefined &&
    field.confidence < 0.6;

  const missing = field.value === null;

  return (
    <div
      className={`rounded-xl border p-5 shadow

      ${
        missing
          ? "border-red-300 bg-red-50"
          : lowConfidence
          ? "border-yellow-300 bg-yellow-50"
          : "bg-white"
      }`}
    >
      <div className="flex items-center justify-between">

        <h3 className="text-lg font-bold">

          {field.label}

        </h3>

        {accepted && (
          <span className="rounded bg-green-200 px-3 py-1">
            Accepted
          </span>
        )}

        {rejected && (
          <span className="rounded bg-red-200 px-3 py-1">
            Rejected
          </span>
        )}

      </div>

      <textarea
        value={value ?? ""}
        onChange={(e) => setValue(e.target.value)}
        rows={3}
        className="mt-4 w-full rounded border p-3"
      />

      {field.source && (
        <p className="mt-3 text-sm text-gray-500">
          Source: {field.source}
        </p>
      )}

      {field.source_date && (
        <p className="text-sm text-blue-600">
          News Date: {field.source_date}
        </p>
      )}

      {field.confidence !== undefined && (
        <p className="mt-3 font-medium">
          Confidence: {(field.confidence * 100).toFixed(0)}%
        </p>
      )}

      {field.note && (
        <p className="mt-2 text-red-600">
          {field.note}
        </p>
      )}

      <div className="mt-5 flex gap-3">

        <button
          onClick={() => {
            setAccepted(true);
            setRejected(false);
          }}
          className="rounded bg-green-600 px-4 py-2 text-white"
        >
          Accept
        </button>

        <button
          onClick={() => {
            setRejected(true);
            setAccepted(false);
          }}
          className="rounded bg-red-600 px-4 py-2 text-white"
        >
          Reject
        </button>

      </div>

    </div>
  );
}