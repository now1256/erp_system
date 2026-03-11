"use client";

import { useEffect, useState } from "react";

import { ErpShell } from "@/components/erp-shell";
import { FilterBar } from "@/components/filter-bar";
import { ModuleHeader } from "@/components/module-header";
import { SectionTable } from "@/components/section-table";
import { StockMovementForm } from "@/components/stock-movement-form";
import { getItems, getPartners, getStockMovements, type ItemSummary, type PartnerSummary, type StockMovementSummary } from "@/lib/api";

export default function MovementPage() {
  const [query, setQuery] = useState("");
  const [movementType, setMovementType] = useState("");
  const [items, setItems] = useState<ItemSummary[]>([]);
  const [partners, setPartners] = useState<PartnerSummary[]>([]);
  const [rows, setRows] = useState<StockMovementSummary[]>([]);

  async function load() {
    const [itemList, partnerList, movementList] = await Promise.all([
      getItems(),
      getPartners(),
      getStockMovements({ q: query, movement_type: movementType || undefined }),
    ]);
    setItems(itemList);
    setPartners(partnerList);
    setRows(movementList);
  }

  useEffect(() => {
    load();
  }, [query, movementType]);

  return (
    <ErpShell>
      <ModuleHeader title="재고이력" description="입고, 출고, 조정 이력을 조회하고 등록합니다." />
      <section className="erp-grid">
        <div className="erp-stack">
          <FilterBar
            query={query}
            onQueryChange={setQuery}
            secondary={
              <select className="filter-select" value={movementType} onChange={(e) => setMovementType(e.target.value)}>
                <option value="">전체 구분</option>
                <option value="inbound">입고</option>
                <option value="outbound">출고</option>
                <option value="adjustment">조정</option>
              </select>
            }
          />
          <SectionTable title="재고이력 목록" columns={["일시", "구분", "품목", "수량", "창고", "거래처", "사유"]}>
            {rows.map((row) => (
              <tr key={row.id}>
                <td>{row.moved_at.slice(0, 16).replace("T", " ")}</td>
                <td>{row.movement_type}</td>
                <td>{row.item_name}</td>
                <td>{row.quantity}</td>
                <td>{row.warehouse_name}</td>
                <td>{row.partner_name ?? "-"}</td>
                <td>{row.reason ?? row.reference ?? "-"}</td>
              </tr>
            ))}
          </SectionTable>
        </div>
        <div className="erp-stack">
          <StockMovementForm items={items} partners={partners} onSuccess={load} />
        </div>
      </section>
    </ErpShell>
  );
}
