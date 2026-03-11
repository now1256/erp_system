"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { ReactNode, useEffect, useState } from "react";

import { getCurrentUser, type CurrentUser } from "@/lib/api";
import { clearStoredToken, getStoredToken } from "@/lib/auth";

const navItems = [
  { href: "/dashboard", label: "대시보드" },
  { href: "/inventory", label: "재고현황" },
  { href: "/inventory/movements", label: "재고이력" },
  { href: "/items", label: "품목관리" },
  { href: "/partners", label: "거래처관리" },
];

export function ErpShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const token = getStoredToken();
    if (!token) {
      router.replace("/login");
      return;
    }

    getCurrentUser(token)
      .then((result) => {
        setUser(result);
        setReady(true);
      })
      .catch(() => {
        clearStoredToken();
        router.replace("/login");
      });
  }, [router]);

  function handleLogout() {
    clearStoredToken();
    router.replace("/login");
  }

  if (!ready) {
    return (
      <main className="mx-auto flex min-h-screen max-w-5xl items-center px-4 py-10">
        <div className="border border-[var(--border)] bg-white p-8">
          <h1 className="text-2xl font-semibold">인증 정보를 확인하는 중입니다.</h1>
        </div>
      </main>
    );
  }

  return (
    <div className="erp-shell">
      <aside className="erp-sidebar">
        <div className="erp-brand">
          <strong>조경 ERP</strong>
          <span>재고 · 자재 · 거래처 운영</span>
        </div>
        <nav className="erp-nav">
          {navItems.map((item) => (
            <Link key={item.href} className={pathname === item.href ? "active" : ""} href={item.href}>
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>

      <main className="erp-main">
        <header className="erp-topbar">
          <div className="topbar-meta">
            <span>법인: 그린스케이프 조경</span>
            <span>사용자: {user?.full_name}</span>
            <span>권한: {user?.role}</span>
          </div>
          <div className="topbar-actions">
            <div className="topbar-status">시스템 정상</div>
            <button className="secondary-button" onClick={handleLogout} type="button">
              로그아웃
            </button>
          </div>
        </header>

        <div className="erp-content">{children}</div>
      </main>
    </div>
  );
}
