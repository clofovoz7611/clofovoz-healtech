import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ClofoVoz HealTech AI | Análisis Acústico Clínico",
  description: "Plataforma SaaS para evaluación fonética y biomarcadores vocales",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className="bg-slate-950 text-slate-100 antialiased">{children}</body>
    </html>
  );
}