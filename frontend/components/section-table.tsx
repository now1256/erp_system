import { ReactNode } from "react";

type SectionTableProps = {
  title: string;
  description?: string;
  columns: string[];
  children: ReactNode;
};

export function SectionTable({ title, description, columns, children }: SectionTableProps) {
  return (
    <section className="erp-section">
      <div className="section-header">
        <div>
          <h2>{title}</h2>
          {description ? <p>{description}</p> : null}
        </div>
      </div>
      <div className="erp-table-wrap">
        <table className="erp-table">
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column}>{column}</th>
              ))}
            </tr>
          </thead>
          <tbody>{children}</tbody>
        </table>
      </div>
    </section>
  );
}
