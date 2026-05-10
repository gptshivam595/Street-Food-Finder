interface LoadingStateProps {
  message?: string;
}

export function LoadingState({ message = 'Finding fresh street food...' }: LoadingStateProps) {
  return (
    <div className="space-y-4">
      <p className="text-sm font-semibold text-slate-600">{message}</p>
      <div className="grid gap-4 md:grid-cols-3">
        {Array.from({ length: 3 }, (_, index) => (
          <div key={index} className="rounded-2xl border border-orange-100 bg-white p-5 shadow-sm">
            <div className="animate-pulse space-y-4">
              <div className="h-5 w-24 rounded-full bg-orange-100" />
              <div className="h-6 w-3/4 rounded bg-slate-100" />
              <div className="h-4 w-1/2 rounded bg-slate-100" />
              <div className="flex gap-2">
                <div className="h-7 w-20 rounded-full bg-yellow-100" />
                <div className="h-7 w-20 rounded-full bg-yellow-100" />
              </div>
              <div className="h-10 rounded-full bg-orange-100" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
