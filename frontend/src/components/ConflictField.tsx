"use client";

import { useState } from "react";

import { ProfileField } from "@/types/profile";

interface Props {
  field: ProfileField;
}

export default function ConflictField({
  field,
}: Props) {

  const [selected, setSelected] = useState(0);

  return (
    <div className="rounded-xl border border-orange-300 bg-orange-50 p-5">

      <h3 className="text-lg font-bold">

        {field.label}

      </h3>

      <p className="mb-4 text-sm text-orange-700">

        Multiple values found.
        Please choose one.

      </p>

      {field.candidates?.map(
        (candidate, index) => (

          <label
            key={index}
            className="mb-3 flex cursor-pointer items-start gap-3 rounded border bg-white p-3"
          >

            <input
              type="radio"
              checked={selected === index}
              onChange={() =>
                setSelected(index)
              }
            />

            <div>

              <div className="font-semibold">

                {candidate.value}

              </div>

              <div className="text-sm text-gray-500">

                {candidate.source}

              </div>

              <div className="text-xs">

                Confidence

                {" "}

                {(candidate.confidence * 100).toFixed(0)}%

              </div>

            </div>

          </label>

        )
      )}

    </div>
  );
}