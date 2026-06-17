export default function LungIcon({ className, size = 24, strokeWidth = 2.2, ...props }) {
  return (
    <svg
      viewBox="0 0 48 48"
      className={className}
      width={className ? undefined : size}
      height={className ? undefined : size}
      fill="none"
      aria-hidden="true"
      {...props}
    >
      <path d="M24 5v19" stroke="currentColor" strokeWidth={strokeWidth} strokeLinecap="round" />
      <path
        d="M24 23c-3.2 0-5.7 2-8 5.6"
        stroke="currentColor"
        strokeWidth={strokeWidth}
        strokeLinecap="round"
      />
      <path
        d="M24 23c3.2 0 5.7 2 8 5.6"
        stroke="currentColor"
        strokeWidth={strokeWidth}
        strokeLinecap="round"
      />
      <path
        d="M20 12c-7.2 2.1-12 9-12 19 0 7 4 11 9 11 3 0 5-2.2 5-5.2V13.6c0-1.2-.9-2-2-1.6Z"
        fill="currentColor"
        fillOpacity="0.14"
        stroke="currentColor"
        strokeWidth={strokeWidth}
        strokeLinejoin="round"
      />
      <path
        d="M28 12c7.2 2.1 12 9 12 19 0 7-4 11-9 11-3 0-5-2.2-5-5.2V13.6c0-1.2.9-2 2-1.6Z"
        fill="currentColor"
        fillOpacity="0.14"
        stroke="currentColor"
        strokeWidth={strokeWidth}
        strokeLinejoin="round"
      />
      <path
        d="M15 29c3.4-1.2 5.8-3.2 7-6"
        stroke="currentColor"
        strokeWidth={strokeWidth}
        strokeLinecap="round"
      />
      <path
        d="M33 29c-3.4-1.2-5.8-3.2-7-6"
        stroke="currentColor"
        strokeWidth={strokeWidth}
        strokeLinecap="round"
      />
    </svg>
  );
}
