"use client";

interface LoadingProps {
  size?: "sm" | "md" | "lg";
  text?: string;
  fullScreen?: boolean;
}

export default function Loading({
  size = "md",
  text,
  fullScreen = false,
}: LoadingProps) {
  const sizeClasses = {
    sm: "h-4 w-4 border-2",
    md: "h-8 w-8 border-4",
    lg: "h-12 w-12 border-4",
  };

  const spinnerClass = `animate-spin ${sizeClasses[size]} border-primary border-t-transparent rounded-full`;

  const content = (
    <div className="flex flex-col items-center justify-center space-y-4">
      <div className={spinnerClass}></div>
      {text && (
        <p className="text-gray-600 text-sm font-medium animate-pulse-slow">
          {text}
        </p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-white bg-opacity-90 flex items-center justify-center z-50 animate-fadeIn">
        {content}
      </div>
    );
  }

  return <div className="py-12 animate-fadeIn">{content}</div>;
}
