"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { login } from "@/lib/api";
import { getStoredToken, setStoredToken } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin1234");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (getStoredToken()) {
      router.replace("/dashboard");
    }
  }, [router]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    try {
      const result = await login(username, password);
      setStoredToken(result.access_token);
      router.replace("/dashboard");
    } catch (loginError) {
      setError(loginError instanceof Error ? loginError.message : "로그인에 실패했습니다.");
    }
  }

  return (
    <main className="login-shell">
      <section className="login-panel">
        <div className="login-copy">
          <h1>조경 ERP 로그인</h1>
          <p>재고, 입출고, 품목, 거래처 관리를 위한 운영 포털입니다.</p>
          <div className="login-hint">
            <span>기본 계정</span>
            <strong>admin / admin1234</strong>
          </div>
        </div>
        <form className="login-form" onSubmit={handleSubmit}>
          <label>아이디</label>
          <input value={username} onChange={(event) => setUsername(event.target.value)} />
          <label>비밀번호</label>
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          {error ? <p className="form-error">{error}</p> : null}
          <button className="primary-button" type="submit">로그인</button>
        </form>
      </section>
    </main>
  );
}
