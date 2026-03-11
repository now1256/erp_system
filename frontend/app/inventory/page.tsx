"use client";

import { useEffect, useState } from "react";

import { ErpShell } from "@/components/erp-shell";
import { FilterBar } from "@/components/filter-bar";
import { ModuleHeader } from "@/components/module-header";
import { SectionTable } from "@/components/section-table";
import { getInventoryBalances, type InventoryBalanceSummary } from "@/lib/api";

export default function InventoryPage() {
  const [query, setQuery] = useState("");
  const [lowStockOnly, setLowStockOnly] = useState(false);
  const [rows, setRows] = useState<InventoryBalanceSummary[]>([]);

  useEffect(() => {
    getInventoryBalances({ q: query, low_stock_only: lowStockOnly }).then(setRows);
  }, [query, lowStockOnly]);

  return (
    <ErpShell>
      <ModuleHeader title="재고현황" description="품목명, 품목코드, 창고 기준으로 재고를 조회합니다." />
      <FilterBar
        query={query}
        onQueryChange={setQuery}
        secondary={
          <label className="checkbox-inline">
            <input checked={lowStockOnly} onChange={(e) => setLowStockOnly(e.target.checked)} type="checkbox" />
            저재고만 보기
          </label>
        }
      />
      <SectionTable title="현재고 목록" columns={["품목코드", "품목명", "창고", "위치", "현재고", "가용"]}>
        {rows.map((row) => (
          <tr key={row.id}>
            <td>{row.sku}</td>
            <td>{row.item_name}</td>
            <td>{row.warehouse_name}</td>
            <td>{row.storage_location ?? "-"}</td>
            <td>{row.on_hand_quantity} {row.unit_of_measure}</td>
            <td>{row.available_quantity}</td>
          </tr>
        ))}
      </SectionTable>
    </ErpShell>
  );
}
