"use client";

import { FormEvent, useEffect, useState } from "react";

import { createItem, updateItem, type ItemPayload, type ItemSummary } from "@/lib/api";
import { getStoredToken } from "@/lib/auth";

const categories = [
  { value: "pesticide", label: "농약" },
  { value: "fertilizer", label: "비료" },
  { value: "seed", label: "종자" },
  { value: "material", label: "자재" },
];

type Props = {
  selectedItem: ItemSummary | null;
  onSaved: () => Promise<void>;
};

const defaultForm: ItemPayload = {
  sku: "",
  name: "",
  category: "material",
  manufacturer: "",
  unit_of_measure: "개",
  package_size: "",
  storage_location: "",
  lot_code: "",
  expiration_date: "",
  reorder_threshold: 0,
  notes: "",
  epa_registration_number: "",
  active_ingredient: "",
  signal_word: "",
  npk_grade: "",
  guaranteed_analysis: "",
};

export function ItemForm({ selectedItem, onSaved }: Props) {
  const [form, setForm] = useState<ItemPayload>(defaultForm);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!selectedItem) {
      setForm(defaultForm);
      return;
    }
    setForm({
      sku: selectedItem.sku,
      name: selectedItem.name,
      category: selectedItem.category,
      manufacturer: selectedItem.manufacturer ?? "",
      unit_of_measure: selectedItem.unit_of_measure,
      package_size: selectedItem.package_size ?? "",
      storage_location: selectedItem.storage_location ?? "",
      lot_code: selectedItem.lot_code ?? "",
      expiration_date: selectedItem.expiration_date ?? "",
      reorder_threshold: selectedItem.reorder_threshold,
      notes: "",
      epa_registration_number: selectedItem.epa_registration_number ?? "",
      active_ingredient: selectedItem.active_ingredient ?? "",
      signal_word: selectedItem.signal_word ?? "",
      npk_grade: selectedItem.npk_grade ?? "",
      guaranteed_analysis: selectedItem.guaranteed_analysis ?? "",
    });
  }, [selectedItem]);

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
      if (selectedItem) {
        await updateItem(token, selectedItem.id, form);
        setMessage("품목이 수정되었습니다.");
      } else {
        await createItem(token, form);
        setMessage("품목이 등록되었습니다.");
        setForm(defaultForm);
      }
      await onSaved();
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "품목 저장에 실패했습니다.");
    }
  }

  return (
    <section className="erp-section">
      <div className="section-header">
        <div>
          <h2>{selectedItem ? "품목 수정" : "품목 등록"}</h2>
          <p>농약, 비료, 자재 기본정보를 관리합니다.</p>
        </div>
      </div>
      <form className="form-grid" onSubmit={handleSubmit}>
        <div className="form-row two-col">
          <div>
            <label>품목코드</label>
            <input value={form.sku} onChange={(e) => setForm({ ...form, sku: e.target.value })} />
          </div>
          <div>
            <label>품목명</label>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          </div>
        </div>
        <div className="form-row two-col">
          <div>
            <label>구분</label>
            <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
              {categories.map((category) => (
                <option key={category.value} value={category.value}>
                  {category.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>제조사</label>
            <input value={form.manufacturer} onChange={(e) => setForm({ ...form, manufacturer: e.target.value })} />
          </div>
        </div>
        <div className="form-row two-col">
          <div>
            <label>단위</label>
            <input value={form.unit_of_measure} onChange={(e) => setForm({ ...form, unit_of_measure: e.target.value })} />
          </div>
          <div>
            <label>포장단위</label>
            <input value={form.package_size} onChange={(e) => setForm({ ...form, package_size: e.target.value })} />
          </div>
        </div>
        <div className="form-row two-col">
          <div>
            <label>보관위치</label>
            <input value={form.storage_location} onChange={(e) => setForm({ ...form, storage_location: e.target.value })} />
          </div>
          <div>
            <label>재주문 기준</label>
            <input type="number" value={form.reorder_threshold} onChange={(e) => setForm({ ...form, reorder_threshold: Number(e.target.value) })} />
          </div>
        </div>
        <div className="form-row two-col">
          <div>
            <label>로트</label>
            <input value={form.lot_code} onChange={(e) => setForm({ ...form, lot_code: e.target.value })} />
          </div>
          <div>
            <label>만료일</label>
            <input type="date" value={form.expiration_date} onChange={(e) => setForm({ ...form, expiration_date: e.target.value })} />
          </div>
        </div>
        <div className="form-row two-col">
          <div>
            <label>EPA 등록번호</label>
            <input value={form.epa_registration_number} onChange={(e) => setForm({ ...form, epa_registration_number: e.target.value })} />
          </div>
          <div>
            <label>유효성분 / NPK</label>
            <input
              value={form.category === "fertilizer" ? form.npk_grade : form.active_ingredient}
              onChange={(e) =>
                setForm(
                  form.category === "fertilizer"
                    ? { ...form, npk_grade: e.target.value }
                    : { ...form, active_ingredient: e.target.value },
                )
              }
            />
          </div>
        </div>
        {message ? <p className="form-message">{message}</p> : null}
        {error ? <p className="form-error">{error}</p> : null}
        <div className="form-actions">
          <button className="primary-button" type="submit">
            {selectedItem ? "품목 수정" : "품목 등록"}
          </button>
        </div>
      </form>
    </section>
  );
}
