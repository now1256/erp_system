const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type CurrentUser = {
  id: number;
  username: string;
  full_name: string;
  role: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
  user: CurrentUser;
};

export type DashboardOverview = {
  total_items: number;
  total_stock_on_hand: number;
  low_stock_count: number;
  category_breakdown: { category: string; count: number }[];
  recent_movements: {
    id: number;
    item_name: string;
    movement_type: string;
    quantity: number;
    warehouse_name: string;
    moved_at: string;
  }[];
  inventory_snapshot: {
    sku: string;
    name: string;
    category: string;
    storage_location: string;
    on_hand_quantity: number;
    unit_of_measure: string;
  }[];
};

export type ItemSummary = {
  id: number;
  sku: string;
  name: string;
  category: string;
  manufacturer: string | null;
  unit_of_measure: string;
  package_size: string | null;
  storage_location: string | null;
  lot_code: string | null;
  expiration_date: string | null;
  reorder_threshold: number;
  epa_registration_number: string | null;
  active_ingredient: string | null;
  signal_word: string | null;
  npk_grade: string | null;
  guaranteed_analysis: string | null;
};

export type ItemPayload = {
  sku: string;
  name: string;
  category: string;
  manufacturer?: string;
  unit_of_measure: string;
  package_size?: string;
  storage_location?: string;
  lot_code?: string;
  expiration_date?: string;
  reorder_threshold: number;
  notes?: string;
  epa_registration_number?: string;
  active_ingredient?: string;
  signal_word?: string;
  npk_grade?: string;
  guaranteed_analysis?: string;
};

export type InventoryBalanceSummary = {
  id: number;
  item_id: number;
  item_name: string;
  sku: string;
  warehouse_name: string;
  on_hand_quantity: number;
  reserved_quantity: number;
  available_quantity: number;
  unit_of_measure: string;
  storage_location: string | null;
};

export type StockMovementSummary = {
  id: number;
  item_name: string;
  sku: string;
  movement_type: string;
  quantity: number;
  warehouse_name: string;
  reference: string | null;
  reason: string | null;
  moved_at: string;
  partner_name: string | null;
};

export type StockMovementCreate = {
  item_id: number;
  movement_type: "inbound" | "outbound" | "adjustment";
  quantity: number;
  warehouse_name: string;
  partner_id?: number;
  reference?: string;
  reason?: string;
  memo?: string;
};

export type PartnerSummary = {
  id: number;
  name: string;
  partner_type: string;
  contact_name: string | null;
  phone: string | null;
  address: string | null;
};

export type PartnerPayload = {
  name: string;
  partner_type: string;
  contact_name?: string;
  phone?: string;
  address?: string;
};

type RequestOptions = {
  method?: string;
  token?: string | null;
  body?: unknown;
};

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const headers: HeadersInit = {};
  if (options.body !== undefined) {
    headers["Content-Type"] = "application/json";
  }
  if (options.token) {
    headers.Authorization = `Bearer ${options.token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers,
    cache: "no-store",
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(error?.detail ?? "요청 처리에 실패했습니다.");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export function login(username: string, password: string): Promise<LoginResponse> {
  return request<LoginResponse>("/api/v1/auth/login", { method: "POST", body: { username, password } });
}

export function getCurrentUser(token: string): Promise<CurrentUser> {
  return request<CurrentUser>("/api/v1/auth/me", { token });
}

export function getDashboardOverview(): Promise<DashboardOverview> {
  return request<DashboardOverview>("/api/v1/dashboard/overview");
}

export function getItems(filters?: { q?: string; category?: string }): Promise<ItemSummary[]> {
  const query = new URLSearchParams();
  if (filters?.q) query.set("q", filters.q);
  if (filters?.category) query.set("category", filters.category);
  const suffix = query.toString() ? `?${query.toString()}` : "";
  return request<ItemSummary[]>(`/api/v1/items${suffix}`);
}

export function createItem(token: string, payload: ItemPayload): Promise<ItemSummary> {
  return request<ItemSummary>("/api/v1/items", { method: "POST", token, body: payload });
}

export function updateItem(token: string, itemId: number, payload: ItemPayload): Promise<ItemSummary> {
  return request<ItemSummary>(`/api/v1/items/${itemId}`, { method: "PUT", token, body: payload });
}

export function deleteItem(token: string, itemId: number): Promise<void> {
  return request<void>(`/api/v1/items/${itemId}`, { method: "DELETE", token });
}

export function getInventoryBalances(filters?: { q?: string; low_stock_only?: boolean }): Promise<InventoryBalanceSummary[]> {
  const query = new URLSearchParams();
  if (filters?.q) query.set("q", filters.q);
  if (filters?.low_stock_only) query.set("low_stock_only", "true");
  const suffix = query.toString() ? `?${query.toString()}` : "";
  return request<InventoryBalanceSummary[]>(`/api/v1/inventory/balances${suffix}`);
}

export function getStockMovements(filters?: { q?: string; movement_type?: string }): Promise<StockMovementSummary[]> {
  const query = new URLSearchParams();
  if (filters?.q) query.set("q", filters.q);
  if (filters?.movement_type) query.set("movement_type", filters.movement_type);
  const suffix = query.toString() ? `?${query.toString()}` : "";
  return request<StockMovementSummary[]>(`/api/v1/stock-movements${suffix}`);
}

export function createStockMovement(token: string, payload: StockMovementCreate): Promise<StockMovementSummary> {
  return request<StockMovementSummary>("/api/v1/stock-movements", { method: "POST", token, body: payload });
}

export function getPartners(filters?: { q?: string; partner_type?: string }): Promise<PartnerSummary[]> {
  const query = new URLSearchParams();
  if (filters?.q) query.set("q", filters.q);
  if (filters?.partner_type) query.set("partner_type", filters.partner_type);
  const suffix = query.toString() ? `?${query.toString()}` : "";
  return request<PartnerSummary[]>(`/api/v1/partners${suffix}`);
}

export function createPartner(token: string, payload: PartnerPayload): Promise<PartnerSummary> {
  return request<PartnerSummary>("/api/v1/partners", { method: "POST", token, body: payload });
}

export function updatePartner(token: string, partnerId: number, payload: PartnerPayload): Promise<PartnerSummary> {
  return request<PartnerSummary>(`/api/v1/partners/${partnerId}`, { method: "PUT", token, body: payload });
}

export function deletePartner(token: string, partnerId: number): Promise<void> {
  return request<void>(`/api/v1/partners/${partnerId}`, { method: "DELETE", token });
}
