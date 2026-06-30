interface Props {
    progress: number;
    status: string;
  }
  
  export default function ProgressBar({
    progress,
    status,
  }: Props) {
    return (
      <div className="w-full max-w-xl rounded-xl bg-white p-8 shadow-lg">
  
        <h2 className="text-center text-3xl font-bold">
          Building Company Profile
        </h2>
  
        <p className="mt-3 text-center text-gray-500">
          This usually takes around 40 seconds.
        </p>
  
        <div className="mt-8 h-4 overflow-hidden rounded-full bg-gray-200">
  
          <div
            className="h-full rounded-full bg-blue-600 transition-all duration-500"
            style={{
              width: `${progress}%`,
            }}
          />
  
        </div>
  
        <div className="mt-4 flex justify-between">
  
          <span className="font-medium">
            {status.toUpperCase()}
          </span>
  
          <span className="font-bold">
            {progress}%
          </span>
  
        </div>
  
      </div>
    );
  }