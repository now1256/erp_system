"use client";

import { useEffect, useState } from "react";

import { ErpShell } from "@/components/erp-shell";
import { FilterBar } from "@/components/filter-bar";
import { ItemForm } from "@/components/item-form";
import { ModuleHeader } from "@/components/module-header";
import { SectionTable } from "@/components/section-table";
import { deleteItem, getItems, type ItemSummary } from "@/lib/api";
import { getStoredToken } from "@/lib/auth";

export default function ItemsPage() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [items, setItems] = useState<ItemSummary[]>([]);
  const [selectedItem, setSelectedItem] = useState<ItemSummary | null>(null);

  async function load() {
    setItems(await getItems({ q: query, category: category || undefined }));
  }

  useEffect(() => {
    load();
  }, [query, category]);

  async function handleDelete(itemId: number) {
    const token = getStoredToken();
    if (!token) return;
    await deleteItem(token, itemId);
    if (selectedItem?.id === itemId) {
      setSelectedItem(null);
    }
    await load();
  }

  return (
    <ErpShell>
      <ModuleHeader title="품목관리" description="품목 등록, 수정, 삭제와 기본 검색을 처리합니다." />
      <section className="erp-grid">
        <div className="erp-stack">
          <FilterBar
            query={query}
            onQueryChange={setQuery}
            secondary={
              <select className="filter-select" value={category} onChange={(e) => setCategory(e.target.value)}>
                <option value="">전체 구분</option>
                <option value="pesticide">농약</option>
                <option value="fertilizer">비료</option>
                <option value="material">자재</option>
                <option value="seed">종자</option>
              </select>
            }
          />
          <SectionTable title="품목 목록" columns={["품목코드", "품목명", "구분", "제조사", "단위", "관리"]}>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.sku}</td>
                <td>{item.name}</td>
                <td>{item.category}</td>
                <td>{item.manufacturer ?? "-"}</td>
                <td>{item.unit_of_measure}</td>
                <td className="table-actions">
                  <button className="table-link" onClick={() => setSelectedItem(item)} type="button">수정</button>
                  <button className="table-link danger" onClick={() => handleDelete(item.id)} type="button">삭제</button>
                </td>
              </tr>
            ))}
          </SectionTable>
        </div>
        <div className="erp-stack">
          <ItemForm selectedItem={selectedItem} onSaved={load} />
        </div>
      </section>
    </ErpShell>
  );
}
