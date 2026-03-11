"use client";

import { FormEvent, useEffect, useState } from "react";

import { createStockMovement, type ItemSummary, type PartnerSummary } from "@/lib/api";
import { getStoredToken } from "@/lib/auth";

type StockMovementFormProps = {
  items: ItemSummary[];
  partners: PartnerSummary[];
  onSuccess: () => Promise<void>;
};

type MovementType = "inbound" | "outbound" | "adjustment";

const formTitles: Record<MovementType, string> = {
  inbound: "입고 등록",
  outbound: "출고 등록",
  adjustment: "재고조정",
};

const reasonPlaceholders: Record<MovementType, string> = {
  inbound: "예: 봄철 자재 입고",
  outbound: "예: 현장 사용 출고",
  adjustment: "예: 실사 결과 반영",
};

export function StockMovementForm({ items, partners, onSuccess }: StockMovementFormProps) {
  const [movementType, setMovementType] = useState<MovementType>("inbound");
  const [itemId, setItemId] = useState<number>(items[0]?.id ?? 0);
  const [partnerId, setPartnerId] = useState<number | "">("");
  const [warehouseName, setWarehouseName] = useState("본사 창고");
  const [quantity, setQuantity] = useState("1");
  const [reference, setReference] = useState("");
  const [reason, setReason] = useState("");
  const [memo, setMemo] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!itemId && items[0]) {
      setItemId(items[0].id);
    }
  }, [itemId, items]);

  async function submitMovement() {
    const token = getStoredToken();
    if (!token) {
      throw new Error("로그인이 필요합니다.");
    }
    await createStockMovement(token, {
        item_id: itemId,
        movement_type: movementType,
        quantity: Number(quantity),
        warehouse_name: warehouseName,
        partner_id: partnerId === "" ? undefined : Number(partnerId),
        reference: reference || undefined,
        reason: reason || undefined,
        memo: memo || undefined,
    });
  }

  async function handleRealSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setMessage(null);
    setError(null);

    try {
      await submitMovement();
      setQuantity("1");
      setReference("");
      setReason("");
      setMemo("");
      setPartnerId("");
      setMessage(`${formTitles[movementType]} 처리가 완료되었습니다.`);
      await onSuccess();
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "처리에 실패했습니다.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="erp-section">
      <div className="section-header">
        <div>
          <h2>재고 처리 등록</h2>
          <p>입고, 출고, 조정 내역을 등록하면 현재고와 이력이 즉시 반영됩니다.</p>
        </div>
      </div>
      <form className="form-grid" onSubmit={handleRealSubmit}>
        <div className="form-row form-tabs">
          {(["inbound", "outbound", "adjustment"] as MovementType[]).map((type) => (
            <button
              key={type}
              className={`form-tab ${movementType === type ? "active" : ""}`}
              onClick={() => setMovementType(type)}
              type="button"
            >
              {formTitles[type]}
            </button>
          ))}
        </div>

        <div className="form-row">
          <label>품목</label>
          <select value={itemId} onChange={(event) => setItemId(Number(event.target.value))}>
            {items.map((item) => (
              <option key={item.id} value={item.id}>
                {item.name} ({item.sku})
              </option>
            ))}
          </select>
        </div>

        <div className="form-row">
          <label>창고</label>
          <input value={warehouseName} onChange={(event) => setWarehouseName(event.target.value)} />
        </div>

        <div className="form-row two-col">
          <div>
            <label>{movementType === "adjustment" ? "조정 후 재고" : "수량"}</label>
            <input
              inputMode="decimal"
              min="0"
              step="0.01"
              type="number"
              value={quantity}
              onChange={(event) => setQuantity(event.target.value)}
            />
          </div>
          <div>
            <label>거래처</label>
            <select value={partnerId} onChange={(event) => setPartnerId(event.target.value ? Number(event.target.value) : "")}>
              <option value="">선택 안 함</option>
              {partners.map((partner) => (
                <option key={partner.id} value={partner.id}>
                  {partner.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-row two-col">
          <div>
            <label>참조번호</label>
            <input
              placeholder={movementType === "inbound" ? "예: PO-2026-004" : movementType === "outbound" ? "예: WO-2026-010" : "예: ADJ-2026-002"}
              value={reference}
              onChange={(event) => setReference(event.target.value)}
            />
          </div>
          <div>
            <label>사유</label>
            <input placeholder={reasonPlaceholders[movementType]} value={reason} onChange={(event) => setReason(event.target.value)} />
          </div>
        </div>

        <div className="form-row">
          <label>메모</label>
          <textarea rows={3} value={memo} onChange={(event) => setMemo(event.target.value)} />
        </div>

        {message ? <p className="form-message">{message}</p> : null}
        {error ? <p className="form-error">{error}</p> : null}

        <div className="form-actions">
          <button className="primary-button" disabled={submitting || !itemId} type="submit">
            {submitting ? "처리 중..." : `${formTitles[movementType]} 저장`}
          </button>
        </div>
      </form>
    </section>
  );
}
