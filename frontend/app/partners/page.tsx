"use client";

import { useEffect, useState } from "react";

import { ErpShell } from "@/components/erp-shell";
import { FilterBar } from "@/components/filter-bar";
import { ModuleHeader } from "@/components/module-header";
import { PartnerForm } from "@/components/partner-form";
import { SectionTable } from "@/components/section-table";
import { deletePartner, getPartners, type PartnerSummary } from "@/lib/api";
import { getStoredToken } from "@/lib/auth";

export default function PartnersPage() {
  const [query, setQuery] = useState("");
  const [partnerType, setPartnerType] = useState("");
  const [partners, setPartners] = useState<PartnerSummary[]>([]);
  const [selectedPartner, setSelectedPartner] = useState<PartnerSummary | null>(null);

  async function load() {
    setPartners(await getPartners({ q: query, partner_type: partnerType || undefined }));
  }

  useEffect(() => {
    load();
  }, [query, partnerType]);

  async function handleDelete(partnerId: number) {
    const token = getStoredToken();
    if (!token) return;
    await deletePartner(token, partnerId);
    if (selectedPartner?.id === partnerId) {
      setSelectedPartner(null);
    }
    await load();
  }

  return (
    <ErpShell>
      <ModuleHeader title="거래처관리" description="공급처와 고객사 정보를 등록, 수정, 삭제합니다." />
      <section className="erp-grid">
        <div className="erp-stack">
          <FilterBar
            query={query}
            onQueryChange={setQuery}
            secondary={
              <select className="filter-select" value={partnerType} onChange={(e) => setPartnerType(e.target.value)}>
                <option value="">전체 구분</option>
                <option value="supplier">공급처</option>
                <option value="customer">고객사</option>
              </select>
            }
          />
          <SectionTable title="거래처 목록" columns={["구분", "거래처명", "담당자", "연락처", "관리"]}>
            {partners.map((partner) => (
              <tr key={partner.id}>
                <td>{partner.partner_type}</td>
                <td>{partner.name}</td>
                <td>{partner.contact_name ?? "-"}</td>
                <td>{partner.phone ?? "-"}</td>
                <td className="table-actions">
                  <button className="table-link" onClick={() => setSelectedPartner(partner)} type="button">수정</button>
                  <button className="table-link danger" onClick={() => handleDelete(partner.id)} type="button">삭제</button>
                </td>
              </tr>
            ))}
          </SectionTable>
        </div>
        <div className="erp-stack">
          <PartnerForm selectedPartner={selectedPartner} onSaved={load} />
        </div>
      </section>
    </ErpShell>
  );
}
