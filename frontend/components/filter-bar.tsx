"use client";

type FilterBarProps = {
  query: string;
  onQueryChange: (value: string) => void;
  secondary?: React.ReactNode;
  placeholder?: string;
};

export function FilterBar({ query, onQueryChange, secondary, placeholder }: FilterBarProps) {
  return (
    <div className="filter-bar">
      <input
        className="filter-input"
        placeholder={placeholder ?? "검색어를 입력하세요"}
        value={query}
        onChange={(event) => onQueryChange(event.target.value)}
      />
      {secondary}
    </div>
  );
}
