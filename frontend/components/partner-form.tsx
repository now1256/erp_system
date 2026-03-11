"use client";

import { FormEvent, useEffect, useState } from "react";

import { createPartner, updatePartner, type PartnerPayload, type PartnerSummary } from "@/lib/api";
import { getStoredToken } from "@/lib/auth";

type Props = {
  selectedPartner: PartnerSummary | null;
  onSaved: () => Promise<void>;
};

const defaultForm: PartnerPayload = {
  name: "",
  partner_type: "supplier",
  contact_name: "",
  phone: "",
  address: "",
};

export function PartnerForm({ selectedPartner, onSaved }: Props) {
  const [form, setForm] = useState<PartnerPayload>(defaultForm);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!selectedPartner) {
      setForm(defaultForm);
      return;
    }
    setForm({
      name: selectedPartner.name,
      partner_type: selectedPartner.partner_type,
      contact_name: selectedPartner.contact_name ?? "",
      phone: selectedPartner.phone ?? "",
      address: selectedPartner.address ?? "",
    });
  }, [selectedPartner]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const token = getStoredToken();
    if (!token) {
      setError("로그인이 필요합니다.");
      return;
    }
    setMessage(null);
    setError(null);

    try {
      if (selectedPartner) {
        await updatePartner(token, selectedPartner.id, form);
        setMessage("거래처가 수정되었습니다.");
      } else {
        await createPartner(token, form);
        setMessage("거래처가 등록되었습니다.");
        setForm(defaultForm);
      }
      await onSaved();
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "거래처 저장에 실패했습니다.");
    }
  }

  return (
    <section className="erp-section">
      <div className="section-header">
        <div>
          <h2>{selectedPartner ? "거래처 수정" : "거래처 등록"}</h2>
          <p>공급처, 고객사, 현장 거래처 정보를 관리합니다.</p>
        </div>
      </div>
      <form className="form-grid" onSubmit={handleSubmit}>
        <div className="form-row two-col">
          <div>
            <label>거래처명</label>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          </div>
          <div>
            <label>구분</label>
            <select value={form.partner_type} onChange={(e) => setForm({ ...form, partner_type: e.target.value })}>
              <option value="supplier">공급처</option>
              <option value="customer">고객사</option>
            </select>
          </div>
        </div>
        <div className="form-row two-col">
          <div>
            <label>담당자</label>
            <input value={form.contact_name} onChange={(e) => setForm({ ...form, contact_name: e.target.value })} />
          </div>
          <div>
            <label>연락처</label>
            <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          </div>
        </div>
        <div className="form-row">
          <label>주소</label>
          <input value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} />
        </div>
        {message ? <p className="form-message">{message}</p> : null}
        {error ? <p className="form-error">{error}</p> : null}
        <div className="form-actions">
          <button className="primary-button" type="submit">
            {selectedPartner ? "거래처 수정" : "거래처 등록"}
          </button>
        </div>
      </form>
    </section>
  );
}
