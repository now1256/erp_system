import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Landscaping ERP",
  description: "Inventory operations for pesticide, fertilizer, and landscaping materials",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
