"use client";

import { useEffect, useState } from "react";

import { ErpShell } from "@/components/erp-shell";
import { KpiTile } from "@/components/kpi-tile";
import { ModuleHeader } from "@/components/module-header";
import { SectionTable } from "@/components/section-table";
import { getDashboardOverview, getInventoryBalances, getPartners, getStockMovements, type DashboardOverview, type InventoryBalanceSummary, type PartnerSummary, type StockMovementSummary } from "@/lib/api";

type DashboardData = {
  overview: DashboardOverview;
  balances: InventoryBalanceSummary[];
  movements: StockMovementSummary[];
  partners: PartnerSummary[];
};

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    Promise.all([getDashboardOverview(), getInventoryBalances(), getStockMovements(), getPartners()]).then(
      ([overview, balances, movements, partners]) => setData({ overview, balances, movements, partners }),
    );
  }, []);

  return (
    <ErpShell>
      <ModuleHeader title="대시보드" description="조경 ERP 운영 현황을 한눈에 확인합니다." />
      {!data ? (
        <section className="erp-section"><div className="section-header"><div><h2>로딩 중</h2></div></div></section>
      ) : (
        <>
          <section className="kpi-grid">
            <KpiTile label="등록 품목 수" value={`${data.overview.total_items}`} />
            <KpiTile label="전체 현재고" value={`${data.overview.total_stock_on_hand}`} />
            <KpiTile label="부족 품목" value={`${data.overview.low_stock_count}`} tone="warning" />
            <KpiTile label="거래처 수" value={`${data.partners.length}`} />
          </section>
          <section className="erp-grid">
            <SectionTable title="저재고/현재고" columns={["품목코드", "품목명", "현재고", "창고"]}>
              {data.balances.slice(0, 5).map((balance) => (
                <tr key={balance.id}>
                  <td>{balance.sku}</td>
                  <td>{balance.item_name}</td>
                  <td>{balance.available_quantity}</td>
                  <td>{balance.warehouse_name}</td>
                </tr>
              ))}
            </SectionTable>
            <SectionTable title="최근 재고이력" columns={["일시", "구분", "품목", "수량"]}>
              {data.movements.slice(0, 5).map((movement) => (
                <tr key={movement.id}>
                  <td>{movement.moved_at.slice(0, 16).replace("T", " ")}</td>
                  <td>{movement.movement_type}</td>
                  <td>{movement.item_name}</td>
                  <td>{movement.quantity}</td>
                </tr>
              ))}
            </SectionTable>
          </section>
        </>
      )}
    </ErpShell>
  );
}
